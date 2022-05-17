const API = 'http://127.0.0.1:5000/api/movies'

const listMovies = async () => {
    const res = await fetch(API);
    const data = await res.json();
    console.log(data)
};

window.addEventListener('load', function(){
    listMovies();
})

