const Api = {
    getAlbumsNames: function () {
        return sendApiRequest("GET", "albums", {}, "Getting albums");
    },
    getAlbum: function (name) {
        return sendApiRequest("GET", "albums/" + encodeURIComponent(name), {}, "Getting album " + name);
    },
    searchFaceWithImage(albumName, base64Picture) {
        return sendApiRequest("GET", "albums/" + encodeURIComponent(albumName) + "/search", { picture: base64Picture }, "Searching face");
    },
    searchFaceWithFace(albumName, pictureIndex, faceIndex) {
        return sendApiRequest("GET", "albums/" + encodeURIComponent(albumName) + "/search", { pictureIndex, faceIndex }, "Searching face");
    }
};


function sendApiRequest(method, endpoint, parameters, message) {
    return new Promise(function (resolve, reject) {
        console.info("[API] " + message);
        var urlParameters = Object.entries(parameters)
            .filter(([_, v]) => v !== null && v !== undefined)
            .map(([k, v]) =>
                v instanceof Array ? v.map(i => k + "[]=" + encodeURIComponent(i)).join("&") : k + "=" + encodeURIComponent(v)
            ).join("&");
        fetch("http://localhost:5000" + "/api/" + endpoint + "?" + urlParameters, { method })
            .then(res => res.json())
            .then(function (response) {
                if (!response.success) {
                    console.error("[API] " + response.error);
                    reject(response.error);
                } else {
                    resolve(response.data);
                }
            })
            .catch(reject);
    });
}

export default Api;