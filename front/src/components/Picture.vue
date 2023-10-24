<script setup>
import { defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
    picture: Object,
    facesResults: Array
});

const emit = defineEmits(['search-face']);

const faces = computed(() => {
    var faces = [];
    if (props.facesResults == null)
        return props.picture.faces.map((f, i) => ({ rect: f, id: i }));
    for (let f of props.facesResults) {
        faces.push({...f, rect: props.picture.faces[f.id] });
    }
    return faces;
});

function faceToCss(face) {
    var c = Math.tanh(4 * face.similarity - 2) / 2 + 0.5;
    if (isNaN(c))
        c = 0;
    return {
        left: face.rect[0] / props.picture.width * 100 + '%',
        top: face.rect[1] / props.picture.height * 100 + '%',
        width: face.rect[2] / props.picture.width * 100 + '%',
        height: face.rect[3] / props.picture.height * 100 + '%',
        borderColor: 'rgb( ' + (256 - c * 128) + ', ' + (c * 256) + ', 0)'
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
            <div v-for="face in faces" @click="searchFace(face.id)" class="face" :style="faceToCss(face)">
                <div v-if="face.similarity !== undefined" class="similarity">{{ Math.round(face.similarity * 100) }}%</div>
            </div>
        </div>
        {{ picture.faces.length }} visages trouvés
    </div>
</template>

<style lang="scss" scoped>
.picture {
    position: relative;

    img {
        width: 100%;
        vertical-align: top;
    }

    .face {
        position: absolute;
        border: 2px solid white;
        cursor: pointer;

        &:hover {
            background-color: rgba(255, 0, 0, 0.2);
        }

        .similarity {
            position: absolute;
            bottom: 100%;
        }
    }
}
</style>
