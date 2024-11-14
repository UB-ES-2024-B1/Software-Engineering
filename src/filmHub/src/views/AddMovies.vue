<template>
<div class="add-movies">
        <HeaderPage />
        <div class="left-top-container">
            <RadioForm v-model="selectedRadio" />
        </div>

        <form class="form">
            <p class="title">Add Movie</p>
            <p class="message">Fill in the details below to add a new movie to the database.</p>
            <div class="form-content">
                <div class="left-form">
                    <div class="flex" v-if="selectedRadio === 'value-1'">
                        <label>
                            <input
                                class="input"
                                type="text"
                                placeholder="Enter movie name"
                                v-model="movieName"
                            />
                            <span>Movie Name</span>
                        </label>
                    </div>
                    
                    <div v-if="selectedRadio === 'value-2'">
                        <div class="flex">
                            <label>
                                <input
                                    class="input"
                                    type="text"
                                    placeholder="Enter genre"
                                    v-model="genreInput"
                                    @keydown.enter="addGenre"
                                    @keydown="checkCommaOrEnter($event, 'genre')"
                                />
                                <span>Genre</span>
                            </label>
                            <div class="tags">
                                <span v-for="(tag, index) in genres" :key="index" class="tag">
                                    {{ tag }}
                                    <button @click="removeGenre(index)" class="remove-tag">x</button>
                                </span>
                            </div>
                        </div>
                        <div class="flex">
                            <label>
                                <input
                                    class="input"
                                    type="text"
                                    placeholder="Enter cast members"
                                    v-model="castInput"
                                    @keydown.enter="addCast"
                                    @keydown="checkCommaOrEnter($event, 'cast')"
                                />
                                <span>Cast</span>
                            </label>
                            <div class="tags">
                                <span v-for="(tag, index) in cast" :key="index" class="tag">
                                    {{ tag }}
                                    <button @click="removeCast(index)" class="remove-tag">x</button>
                                </span>
                            </div>
                        </div>
                        <div class="flex" id="director-flex">
                            <label>
                                <input
                                    class="input"
                                    type="text"
                                    placeholder="Enter Director"
                                    v-model="directorInput"
                                    @keydown.enter="addDirector"
                                    @keydown="checkCommaOrEnter($event, 'director')"
                                />
                                <span>Director</span>
                            </label>
                            <div class="tags">
                                <span v-for="(tag, index) in director" :key="index" class="tag">
                                    {{ tag }}
                                    <button @click="removeDirector(index)" class="remove-tag">x</button>
                                </span>
                            </div>
                        </div>
                        <div class="flex">
                            <label>
                                <input
                                    class="input"
                                    type="number"
                                    placeholder="Number of Movies"
                                    v-model="numMovies"
                                    min="1"
                                    max="100"
                                />
                                <span>Number of Movies</span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="vertical-line" v-if="selectedRadio === 'value-2'"></div>
                <div class="right-form" v-if="selectedRadio === 'value-2'">
                    <div class="flex">
                        <RatingSlider v-model="rating" />
                    </div>
                    <div class="flex" id="date-flex">
                        <label>
                            <span>Min Release Date</span>
                            <DatePicker v-model="releaseDate" placeholder="dd-mm-yyyy" class="date-1" />
                        </label>
                        <label>
                            <span>Max Release Date</span>
                            <DatePicker v-model="endDate" placeholder="dd-mm-yyyy" class="date-2" />
                        </label>
                    </div>
                </div>
            </div>

            <button class="submit">Submit</button>
        </form>
    </div>
</template>

<script>
import RadioForm from '@/components/RadioForm.vue';
import RatingSlider from '@/components/RatingSlider.vue';
import DatePicker from '@/components/DatePicker.vue';
import HeaderPage from '@/components/HeaderPage.vue';

export default {
    name: 'AddMovies',
    components: {
        RadioForm,
        RatingSlider,
        DatePicker,
        HeaderPage
    },
    data() {
        return {
            selectedRadio: 'value-1',
            movieName: '',
            genreInput: '',
            castInput: '',
            directorInput: '',
            genres: [],
            cast: [],
            director: [],
            rating: 0,
            releaseDate: null,
            endDate: null,
        };
    },
    methods: {
        addGenre() {
            // Remove commas before adding the genre
            const genre = this.genreInput.trim().replace(/,/g, '');
            if (genre && !this.genres.includes(genre)) {
                this.genres.push(genre);
            }
            this.genreInput = ''; // Clear input field after adding tag
        },
        addCast() {
            // Remove commas before adding the cast member
            const castMember = this.castInput.trim().replace(/,/g, '');
            if (castMember && !this.cast.includes(castMember)) {
                this.cast.push(castMember);
            }
            this.castInput = ''; // Clear input field after adding tag
        },
        addDirector() {
            // Remove commas before adding the director
            const director = this.directorInput.trim().replace(/,/g, '');
            if (director && !this.director.includes(director)) {
                this.director.push(director);
            }
            this.directorInput = ''; // Clear input field after adding tag
        },
        checkCommaOrEnter(event, type) {
            if (event.key === ',' || event.key === 'Enter') {
                if (type === 'genre') {
                    this.addGenre();
                } else if (type === 'cast') {
                    this.addCast();
                } else if (type === 'director') {
                    this.addDirector();
                }
                event.preventDefault(); // Prevent default behavior of comma or enter key
            }
        },
        removeGenre(index) {
            this.genres.splice(index, 1);
        },
        removeCast(index) {
            this.cast.splice(index, 1);
        },
        removeDirector(index) {
            this.director.splice(index, 1);
        },
    }
};
</script>

<style scoped>
.add-movies {
    background: #212121;
    height: 100vh;
    display: flex;
    justify-content: center; /* Centra horizontalmente */
    align-items: flex-start; /* Alinea los elementos hacia la parte superior */
    padding-top: 50px; /* Da espacio hacia arriba para que el contenido esté más abajo */
}


.left-top-container {
    margin: 20px;
    margin-top: 50px; /* Añadido para bajar la radio y alinearla con el formulario */
}

.form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 70vw;
    padding: 20px;
    border-radius: 20px;
    position: relative;
    background-color: #1a1a1a;
    color: #fff;
    border: 1px solid #333;
    margin-top: 50px;
}

.title {
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -1px;
    position: relative;
    display: flex;
    align-items: center;
    padding-left: 30px;
    color: #00bfff;
}

.message,
.signin {
    font-size: 14.5px;
    color: rgba(255, 255, 255, 0.7);
}

.form-content {
    display: flex;
    gap: 40px;
}

#director-flex {
    gap: 100px;
}
.tags{
    display: flex;
    flex-wrap: wrap;
    gap: 16;
}

.left-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 35%; /* Reduce width to 35% */
}

.right-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 65%; /* Increase width to 65% */
}

.vertical-line {
    width: 1px;
    background-color: #333;
    height: auto;
}

.flex {
    display: flex;
    flex-direction: column; /* Keep the stack of input and tags vertically */
    width: 100%;
    gap: 15px; /* Increased gap between the fields (genres, cast, director) */
}

.form label {
    position: relative;
}

.form label .input {
    background-color: #333;
    color: #fff;
    width: 100%;
    padding: 20px 5px 5px 10px;
    outline: 0;
    border: 1px solid rgba(105, 105, 105, 0.397);
    border-radius: 10px;
}

.form label .input+span {
    color: rgba(255, 255, 255, 0.5);
    position: absolute;
    left: 10px;
    top: 0px;
    font-size: 0.9em;
    cursor: text;
    transition: 0.4s;
}

.form label .input:focus+span {
    color: rgba(0, 191, 255, 0.94);
    transform: translateY(-25px);
    font-size: 0.8em;
}

.submit {
    background-color: #00bfff;
    border: none;
    color: #fff;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 10px;
    margin-top: 20px;
    align-self: flex-end;
    transition: background-color 0.3s;
}

.submit:hover {
    background-color: #009ac7;
}

.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px; /* Ensures tags appear below the input field */
}

.tag {
    background-color: #333;
    color: #00bfff;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 14px;
    display: flex;
    align-items: center;
}

.remove-tag {
    background: none;
    border: none;
    color: #ffffff;
    margin-left: 5px;
    cursor: pointer;
    font-size: 14px;
}
#date-flex {
    max-width: 200px;
}
</style>
