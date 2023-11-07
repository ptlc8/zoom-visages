<script setup>
import { computed, defineProps, ref, watch } from 'vue'
import Api from '../api.js'

import Picture from './Picture.vue'

const props = defineProps({
    name: String
});

const albumPictures = ref([]);
const searchSourceUrl = ref(null);
const selectedFace = ref(null);
const searchResults = ref(null); // [{picture:0,faces:[{similarity:0.5}]}]
const similarityThreshold = ref(0.5);

const pictures = computed(() => {
    var pictures = [];
    if (searchResults.value == null)
        return albumPictures.value.map((p, i) => ({ picture: p, id: i }));
    for (let p of searchResults.value) {
        if (Math.max(...p.faces.map(f => f.similarity)) < similarityThreshold.value)
            continue;
        pictures.push({ ...p, picture: albumPictures.value[p.id] });
    }
    return pictures;
});

function updateAlbum() {
    Api.getAlbum(props.name).then(album => {
        albumPictures.value = album.pictures;
        searchResults.value = null;
    });
}
updateAlbum();
watch(props, () => {
    updateAlbum();
});

function selectFaceFile() {
    document.getElementById('face-file-input').click();
}

function loadSourceFromFaceFile() {
    var input = document.getElementById('face-file-input');
    if (input.files.length == 0)
        return;
    var reader = new FileReader();
    reader.onload = () => {
        searchSourceUrl.value = reader.result;
        selectedFace.value = { dataURL: reader.result };
    }
    reader.readAsDataURL(input.files[0]);
}

function selectFace(pictureIndex, faceIndex) {
    selectedFace.value = { pictureIndex, faceIndex };
    var img = new Image();
    img.src = '' + albumPictures.value[pictureIndex].path;
    img.onload = () => {
        var picture = albumPictures.value[pictureIndex];
        var face = picture.faces[faceIndex];
        var searchSourceCanvas = document.createElement('canvas');
        var ctx = searchSourceCanvas.getContext('2d');
        var xF = img.naturalWidth / picture.width;
        var yF = img.naturalHeight / picture.height;
        ctx.drawImage(img, face[0] * xF, face[1] * yF, face[2] * xF, face[3] * yF, 0, 0, searchSourceCanvas.width, searchSourceCanvas.height);
        searchSourceUrl.value = searchSourceCanvas.toDataURL();
    };
}

function searchFace() {
    if (selectedFace.value.dataURL) {
        Api.searchFaceWithImage(props.name, selectedFace.value.dataURL.replace(/.*;/,'')).then(results => {
            searchResults.value = results;
        });
    } else if (selectedFace.value.pictureIndex != null) {
        Api.searchFaceWithFace(props.name, selectedFace.value.pictureIndex, selectedFace.value.faceIndex).then(results => {
            searchResults.value = results;
        });
    }
}
</script>

<template>
    <div>
        <h2>{{ name }}</h2>
        <div class="search-face">
            <input @change="loadSourceFromFaceFile" type="file" id="face-file-input" />
            <div class="drop-zone" @click="selectFaceFile">📤 Rechercher un visage avec une photo</div>
            <img v-if="searchSourceUrl" :src="searchSourceUrl" class="source" width="200" height="200" />
            <span v-else class="tip">Clique sur un visage pour le sélectionner</span>
            <div v-if="selectedFace" class="actions">
                <button @click="searchFace">Rechercher ce visage</button>
                <label for="similarity">Seuil de similarité :</label>
                <input v-model="similarityThreshold" id="similarity" type="range" min="0" max="1" step="0.01" />
                <button @click="searchResults = null" v-if="searchResults != null">Annuler</button>
            </div>
        </div>
        <div class="pictures">
            <Picture v-if="pictures" v-for="picture in pictures" :picture="picture.picture" :faces-results="picture.faces" @search-face="selectFace(picture.id, $event.faceIndex)" />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.pictures {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;

    >* {
        flex: 0 1 300px;
        margin: 4px;
    }
}

.search-face {
    display: flex;
    font-size: 1.5em;

    >* {
        flex: 1;
        margin: 4px;
        padding: 4px;
        background-color: #333;
        border-radius: 4px;
    }

    .source {
        flex: 0 0 200px;
    }

    .tip {
        text-align: center;
    }

    .drop-zone {
        border: 2px dashed white;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .actions {
        display: flex;
        flex-direction: column;


        button {

        }
    }

    #face-file-input {
        display: none;
    }
}
</style>