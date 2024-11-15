<template>

    <div class="min-vh-100 d-flex flex-column align-items-center text-white p-5" id="addMoviesPage">
        <HeaderPage class="mb-5" />
        <div class="container">

            <!-- Use flexbox to place RadioForm to the left side of the form -->
            <div class="radio d-flex mb-4">
                <div class="me-4">
                    <RadioForm v-model="formType" />
                </div>
                <main :class="['main-form', 'rounded-3', 'shadow-lg', 'p-4', { 'small-form': formType === 'value-1' }]"
                    id="formBox">
                    <h2 class="fs-4 fw-bolder mb-4">Add Movie</h2>

                    <div v-if="formType === 'value-1'" class="mb-3">
                        <!-- Display single movie name input field if 'Add Movie by Name' is selected -->
                        <label for="movieName" class="form-label">Movie Name</label>
                        <input id="movieName" v-model="movieName" placeholder="Enter movie name" class="form-control" />
                    </div>

                    <div v-else>
                        <!-- Display the full form if 'Add Movie by Features' is selected -->
                        <div class="row g-4">
                            <div class="col-md-5">
                                <div class="mb-3">
                                    <label for="genre" class="form-label">Genre</label>
                                    <div class="d-flex flex-wrap gap-2 mt-2" id="genreListTag">
                                        <span v-for="(genre, index) in genres" :key="index"
                                            class="badge text-sm d-flex align-items-center" id="tagGenre">
                                            {{ genre }}
                                            <button class="btn-close btn-close-white ms-2"
                                                @click="removeItem(index, 'genres')"></button>
                                        </span>
                                    </div>
                                    <div class="input-group mt-2">
                                        <input id="genre" v-model="newGenre" placeholder="Add genre"
                                            class="form-control" @keyup.enter="addItem(newGenre, 'genres')"
                                            @keyup="checkComma(newGenre, 'genres')" />
                                        <button class="btn btn-primary" @click="addItem(newGenre, 'genres')"
                                            id="btn-genre">
                                            <i class='bx bx-plus-medical'></i>
                                        </button>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label for="cast" class="form-label">Cast</label>
                                    <div class="d-flex flex-wrap gap-2 mt-2" id="castListTag">
                                        <span v-for="(member, index) in cast" :key="index"
                                            class="badge text-sm d-flex align-items-center" id="tagMember">
                                            {{ member }}
                                            <button class="btn-close btn-close-white ms-2"
                                                @click="removeItem(index, 'cast')"></button>
                                        </span>
                                    </div>
                                    <div class="input-group mt-2">
                                        <input id="cast" v-model="newCastMember" placeholder="Add cast member"
                                            class="form-control" @keyup.enter="addItem(newCastMember, 'cast')"
                                            @keyup="checkComma(newCastMember, 'cast')" />
                                        <button class="btn btn-primary" @click="addItem(newCastMember, 'cast')"
                                            id="btn-cast">
                                            <i class='bx bx-plus-medical'></i>
                                        </button>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label for="director" class="form-label">Director</label>
                                    <div class="d-flex flex-wrap gap-2 mt-2" id="directorListTag">
                                        <span v-for="(dir, index) in director" :key="index"
                                            class="badge text-sm d-flex align-items-center" id="tagDirector">
                                            {{ dir }}
                                            <button class="btn-close btn-close-white ms-2"
                                                @click="removeItem(index, 'director')"></button>
                                        </span>
                                    </div>
                                    <div class="input-group mt-2">
                                        <input id="director" v-model="newDirector" placeholder="Add a Director"
                                            class="form-control" @keyup.enter="addItem(newDirector, 'director')"
                                            @keyup="checkComma(newDirector, 'director')" />
                                        <button class="btn btn-primary" @click="addItem(newDirector, 'director')"
                                            id="btn-director">
                                            <i class='bx bx-plus-medical'></i>
                                        </button>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label for="movieCount" class="form-label">Number of Movies</label>
                                    <input id="movieCount" v-model="movieCount" type="number" class="form-control"
                                        placeholder="8" />
                                </div>
                            </div>
                            <div class="col-md-1" id="division">
                                <div class="vertical-line"></div>
                            </div>
                            <div class="col-md-5">
                                <div class="mb-3">
                                    <label class="form-label">Movie Rating</label>
                                    <input type="range" v-model.number="rating" min="0" max="5" step="0.1"
                                        class="form-range" id="slidingBar" />
                                    <div class="d-flex justify-content-between mt-2">
                                        <span>0</span>
                                        <span>{{ rating.toFixed(1) }}</span>
                                        <span>5</span>
                                    </div>
                                    <StarRating :rating="6 - Math.floor(rating)" class="star-rating"
                                        @update:rating="updateRating" />
                                </div>

                                <div class="mb-2">
                                    <label for="minDate" class="form-label">Min Release Date</label>
                                    <input id="minDate" v-model="minDate" type="date" class="form-control" />
                                </div>

                                <div class="mb-2">
                                    <label for="maxDate" class="form-label">Max Release Date</label>
                                    <input id="maxDate" v-model="maxDate" type="date" class="form-control" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex justify-content-center" id="submit">
                        <button class="btn-submit btn-dark w-100 mt-3" @click="submitForm">Submit</button>
                    </div>
                </main>
            </div>
        </div>
    </div>
</template>

<script>
import HeaderPage from '@/components/HeaderPage.vue';
import RadioForm from '@/components/RadioForm.vue';
import StarRating from '@/components/StarRating.vue';


export default {
    name: 'AddMovies',
    components: {
        HeaderPage,
        RadioForm,
        StarRating,

    },
    data() {
        return {
            formType: 'value-2', // Default to 'Add Movie by Features'
            movieName: '',
            genres: ['Horror', 'Action'],
            cast: ['John Cena', 'Tom Holland'],
            director: ['Steven Spielberg'],
            rating: 0,
            movieCount: 1,
            minDate: 'dd-mm-yyyy',
            maxDate: 'dd-mm-yyyy',
            newGenre: '',
            newCastMember: '',
            newDirector: '',
        };
    },
    methods: {
        addItem(item, list) {
            if (item && !this[list].includes(item)) {
                this[list].push(item);
                if (list === 'genres') this.newGenre = '';
                if (list === 'cast') this.newCastMember = '';
                if (list === 'director') this.newDirector = '';
            }
        },

        checkComma(input, list) {
            // If the input contains a comma, add the item to the list
            if (input.includes(',')) {
                // Split by commas and add each item
                input.split(',').forEach(item => {
                    const trimmedItem = item.trim();
                    if (trimmedItem && !this[list].includes(trimmedItem)) {
                        this[list].push(trimmedItem);
                    }
                });
                // Reset input field
                if (list === 'genres') this.newGenre = '';
                if (list === 'cast') this.newCastMember = '';
                if (list === 'director') this.newDirector = '';
            }
        },
        removeItem(index, list) {
            this[list].splice(index, 1);
        },
        submitForm() {
            // Handle form submission based on the selected form type
            if (this.formType === 'value-1') {
                console.log({
                    movieName: this.movieName,
                });
            } else {
                console.log({
                    genres: this.genres,
                    cast: this.cast,
                    director: this.director,
                    rating: this.rating,
                    movieCount: this.movieCount,
                    minDate: this.minDate,
                    maxDate: this.maxDate,
                });
            }

            // Clear the fields and lists after submission
            this.movieName = '';
            this.genres = [];
            this.cast = [];
            this.director = [];
            this.rating = 0;
            this.movieCount = 1;
            this.minDate = 'dd-mm-yyyy';
            this.maxDate = 'dd-mm-yyyy';
            this.newGenre = '';
            this.newCastMember = '';
            this.newDirector = '';
        },

        updateRating(newRating) {
            this.rating = newRating;
        }
    },
};
</script>


<style>
.movie-popup {

    z-index: 1000;
}

#addMoviesPage {
background: black;
}
#genreListTag,
#castListTag,
#directorListTag {
    max-height: 100px;
    overflow: auto;
}

.container {
    position: relative;
    /* Establishes a reference point for absolute positioning */
    height: 100vh;
    /* Full height of the viewport */

}

.main-form {
    background-color: rgb(17, 17, 17);
    width: 100%;
    /* Default full width */
}

.main-form.small-form {
    background-color: rgb(17, 17, 17);
    width: 100%;
    /* Full width */
    max-width: 600px;
    /* Maintain the original size with max width */
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    position: absolute;
    /* Absolute positioning to center it */
    top: 40%;
    /* Center vertically */
    left: 50%;
    /* Center horizontally */
    transform: translate(-50%, -50%);
    /* Offset by 50% of its own dimensions */
}

.radio {
    margin-left: -10%;
    margin-top: 10%;

}

.star-rating {
    display: flex;
    padding: 1%;
}

#btn-genre,
#btn-cast,
#btn-director {
    margin-left: 0.3vw;
    background-color: rgba(67, 93, 216, 0.3);
    border: 2px solid rgb(67, 93, 216);
}

#tagGenre,
#tagMember,
#tagDirector {
    background-color: rgba(67, 93, 216, 0.3);
    border: 2px solid rgb(67, 93, 216);
}

#movieCount {
    width: 20%;
}

.vertical-line {
    height: 100%;
    /* Ensure it stretches across the full height of the form */
    background: rgb(88, 85, 85) !important;
    width: 1px !important;
    margin-left: 50%;


}

#division {
    margin-left: 2vw;
    margin-right: 2vw;
}

#slidingBar {
    padding-top: 10%;
    height: 4vh;
}

.btn-submit {
    background-color: rgba(67, 93, 216, 0.3);
    border: 2px solid rgb(67, 93, 216);
    color: aliceblue;
    padding: 0.6vh;
    border-radius: 6px;
    max-width: 50%;
}

.btn-submit:hover {
    background-color: rgba(67, 92, 216, 0.6);
    border: 2px solid rgb(67, 93, 216);
}

.btn-submit:active {
    background-color: rgb(43, 68, 196);
    background-color: rgba(43, 68, 196, 0.9);
}

#submit {
    margin-top: 2vh;
}

.form-control:focus {
    border-color: rgb(67, 93, 216) !important;
    /* Use !important to override Bootstrap styles */
    box-shadow: 0 0 0 0.15rem rgba(120, 133, 206, 0.25);
    /* Optional: Add subtle shadow */
}

.form-label {
    font-weight: 500;
}
</style>
