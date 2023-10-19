<script setup>
import Api from './api.js'
import { ref } from 'vue'

import Album from './components/Album.vue'

const albumsNames = ref([]);
const selectedAlbumName = ref(null);
Api.getAlbumsNames().then(names => {
    albumsNames.value = names;
});
</script>

<template>
    <header>
        <h1>Zoom Visages</h1>
    </header>
    <main>
        <div class="albums">
            <button v-for="albumName in albumsNames" @click="selectedAlbumName = albumName">{{ albumName }}</button>
        </div>
        <Album v-if="selectedAlbumName" :name="selectedAlbumName" />
    </main>
</template>

<style lang="scss">
header {
    background-color: #333;
    color: white;
    padding: 1em;
}
.albums {
    list-style: none;
    display: flex;

    button {
        margin: 0.5em;
        padding: 0.5em;
    }
}
</style>
