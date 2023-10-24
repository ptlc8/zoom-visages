import pickle
import cv2
import dlib
import os
import numpy as np
import base64


# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
# load the face recognition model
face_recognition_model = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')


def detect_face_rects(image):
    return detector(image, 1)

def detect_face_landmarks(image, rect):
    return predictor(image, rect)


# calcule la ressemblance entre deux visages
def calc_similarity(encodings1, encoding2):
    # compute the Euclidean distance between the two encodings of list of arrays
    return 1 - np.linalg.norm(encodings1 - encoding2)

# tester le ressemblance entre deux visages
def similar(encodings1, encoding2, threshold=0.4):
    return calc_similarity(encodings1, encoding2) >= threshold


ROOT_DIR = 'photos'


class Picture:
    def __init__(self, path, encodings, faces, width, height):
        self.path = path
        self.encodings = encodings
        self.faces = faces
        self.width = width
        self.height = height
    
    def __str__(self):
        return self.path
    
    def to_dict(self):
        return { 'path': self.path, 'width': self.width, 'height': self.height, 'faces': [[r.left(), r.top(), r.width(), r.height()] for r in self.faces] }
    
    @staticmethod
    def from_image(image, path=None):
        rects = detect_face_rects(image)
        encodings = [np.array(face_recognition_model.compute_face_descriptor(image, detect_face_landmarks(image, rect), 1)) for rect in rects]
        return Picture(path, encodings, rects, image.shape[1], image.shape[0])
    
    @staticmethod
    def from_file(path, max_pixels=1280*720):
        image = cv2.imread(path)
        if max_pixels != None and image.shape[0] * image.shape[1] > max_pixels:
            scale_factor = np.sqrt(max_pixels / (image.shape[0] * image.shape[1]))
            image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)
        return Picture.from_image(image, path)
    
    @staticmethod
    def from_base64(base64pic, path=None):
        # TODO : ne fonctionne pas :/
        #image = imread(io.BytesIO(base64.b64decode(base64pic)))
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        decode = base64.b64decode(base64pic)
        print(type(decode))
        arr = np.frombuffer(decode, np.uint8)
        print(type(arr))
        image = cv2.imdecode(arr, 0)
        print(type(image))
        return Picture.from_image(image, path)


class Album:
    def __init__(self, name):
        self.name = name
        self.pictures = []
        if os.path.isfile(ROOT_DIR + os.sep + self.name + '.pickle'):
            # si le fichier pickle existe, on le charge
            self.load()
        else:
            # sinon on le crée
            self.update()
        
    def save(self):
        output = open(ROOT_DIR + os.sep + self.name + '.pickle', 'wb')
        # on parcourt tous les dossiers du dataset
        for picture in self.pictures:
            pickle.dump(picture, output)
        output.close()
        
    def load(self):
        with open(ROOT_DIR + os.sep + self.name + '.pickle', 'rb') as f:
            try:
                self.pictures = []
                while True:
                    package = pickle.load(f)
                    self.pictures.append(package)
            except EOFError:
                pass
            
    def update(self):
        print('updating album', self.name)
        self.pictures = []
        # on parcourt toutes les images du dossier
        for image_name in os.listdir(ROOT_DIR + os.sep + self.name):
            print('\t', image_name)
            self.pictures.append(Picture.from_file(ROOT_DIR + os.sep + self.name + os.sep + image_name))
        self.save()
    
    def get_search_by_face(self, faceEncoding):
        result_pictures = []
        for id, picture in enumerate(self.pictures):
            faces = []
            for eId, e in enumerate(picture.encodings):
                faces.append({ 'id': eId, 'similarity': calc_similarity([ faceEncoding ], e) })
            result_pictures.append({ 'id': id, 'faces': faces })
        result_pictures.sort(key=lambda p: -max((f['similarity'] for f in p['faces']), default=0))
        return result_pictures
    
    def to_dict(self):
        return { 'name': self.name, 'pictures': [ p.to_dict() for p in self.pictures ] }
    
    
def get_albums():
    albums = {}
    for album_name in os.listdir(ROOT_DIR):
        if os.path.isdir(ROOT_DIR + os.sep + album_name):
            albums[album_name] = Album(album_name)
    return albums

if __name__ == '__main__':
    get_albums()