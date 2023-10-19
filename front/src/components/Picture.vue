<script setup>
import { defineProps, defineEmits } from 'vue'

var props = defineProps({
    picture: Object
});

var emit = defineEmits(['search-face']);

function faceToCss(face) {
    return {
        left: face[0] / props.picture.width * 100 + '%',
        top: face[1] / props.picture.height * 100 + '%',
        width: face[2] / props.picture.width * 100 + '%',
        height: face[3] / props.picture.height * 100 + '%'
    }
}

function searchFace(faceIndex) {
    emit('search-face', { faceIndex })
}
</script>

<template>
    <div>
        <div class="picture">
            <img :src="'http://localhost:5000/' + picture.path" />
            <div v-for="face, index in picture.faces" @click="searchFace(index)" class="face" :style="faceToCss(face)"></div>
        </div>
        {{ picture.faces.length }} visages trouvés
    </div>
</template>

<style lang="scss" scoped>
.picture {
    position: relative;
    line-height: 0;

    img {
        width: 100%;
    }

    .face {
        position: absolute;
        border: 2px solid red;
        cursor: pointer;

        &:hover {
            background-color: rgba(255, 0, 0, 0.2);
        }
    }
}
</style>
