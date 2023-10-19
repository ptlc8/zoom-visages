<script setup>
import { defineProps, ref, watch } from 'vue'
import Api from '../api.js'

import Picture from './Picture.vue'

var props = defineProps({
    name: String
});

const pictures = ref([]);
const searchSourceUrl = ref(null);
const selectedFace = ref(null);
const searchResults = ref(null);

function updateAlbum() {
    Api.getAlbum(props.name).then(album => {
        pictures.value = album.pictures;
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
    img.src = 'http://localhost:5000/' + pictures.value[pictureIndex].path;
    img.onload = () => {
        var picture = pictures.value[pictureIndex];
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
        Api.searchFaceWithImage(props.name, selectedFace.value.dataURL.replace(/.*;/,'')).then(pictures => {
            searchResults.value = pictures;
        });
    } else if (selectedFace.value.pictureIndex != null) {
        Api.searchFaceWithFace(props.name, selectedFace.value.pictureIndex, selectedFace.value.faceIndex).then(pictures => {
            searchResults.value = pictures;
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
            </div>
        </div>
        <div class="pictures">
            <Picture v-if="pictures" v-for="picture, index in (searchResults || pictures)" :picture="picture" @search-face="selectFace(index, $event.faceIndex)" />
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