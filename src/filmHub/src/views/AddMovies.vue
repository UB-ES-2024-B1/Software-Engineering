<template>
    <div class="add-movies-page">
        <HeaderPage />

        <div id="admin-movie-form" class="card w-100 mx-auto" style="max-width: 640px;">
            <div class="card-header">
                <h5 class="card-title">Add New Movies</h5>
            </div>
            <form @submit.prevent="handleSubmit">
                <div class="card-body">
                    <div class="form-check mb-4">
                        <input type="checkbox" id="batchAdd" v-model="isBatchAdd" class="form-check-input" />
                        <label for="batchAdd" class="form-check-label">Enable Batch Add</label>
                    </div>
                    <!-- Movie Name Input Field (Visible when not batch adding) -->
                    <div v-if="!isBatchAdd" class="mb-4">
                        <label for="movieName" class="form-label">Movie Name</label>
                        <input type="text" id="movieName" v-model="formData.movieName" class="form-control" required placeholder="Movie Name"/>
                    </div>
                    <div v-if="isBatchAdd">
                        <!-- Genre Dropdown -->
                        <div class="mb-4 dropdown-container">
                            <label class="form-label d-flex justify-content-between" @click="toggleDropdown('genre')">
                                Genre
                                <span :class="{ 'rotate-180': dropdownStates.genre }" class="dropdown-arrow"><i
                                        class='bx bxs-chevron-down'></i></span>
                            </label>
                            <div v-if="dropdownStates.genre" class="dropdown-content-genre">
                                <select v-model="selectedGenre" @change="addGenre" class="form-select">
                                    <option value="" disabled>Select genres</option>
                                    <option v-for="g in genres" :key="g">{{ g }}</option>
                                </select>
                                <div class="tag-list mt-2 d-flex flex-wrap gap-2">
                                    <span v-for="g in formData.genre" :key="g" class="tag">
                                        {{ g }}
                                        <button type="button" @click="removeGenre(g)"
                                            class="x-btn btn-close btn-close-white btn-sm"></button>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Date Range Dropdown -->
                        <div class="mb-4 dropdown-container">
                            <label class="form-label d-flex justify-content-between"
                                @click="toggleDropdown('dateRange')">
                                Date Range
                                <span :class="{ 'rotate-180': dropdownStates.dateRange }" class="dropdown-arrow"><i
                                        class='bx bxs-chevron-down'></i></span>
                            </label>
                            <div v-if="dropdownStates.dateRange" class="dropdown-content">
                                <div class="d-flex gap-3">
                                    <div class="position-relative">
                                        <DatePicker v-model="formData.startDate" label="Start Date" id="start-date"
                                            inputClass="date-form mb-2" />
                                        <i
                                            class="bx bx-calendar-alt calendar-icon position-absolute top-50 end-0 translate-middle-y me-2"></i>
                                    </div>
                                    <div class="position-relative">
                                        <DatePicker v-model="formData.endDate" label="End Date" id="end-date"
                                            inputClass="date-form mb-2" />
                                        <i
                                            class="bx bx-calendar-alt calendar-icon position-absolute top-50 end-0 translate-middle-y me-2"></i>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Director Dropdown -->
                        <div class="mb-4 dropdown-container">
                            <label class="form-label d-flex justify-content-between"
                                @click="toggleDropdown('director')">
                                Director
                                <span :class="{ 'rotate-180': dropdownStates.director }" class="dropdown-arrow"><i
                                        class='bx bxs-chevron-down'></i></span>
                            </label>
                            <div v-if="dropdownStates.director" class="dropdown-content">
                                <input type="text" id="director" v-model="formData.director"
                                    placeholder="Enter director name" class="form-control" />
                            </div>
                        </div>

                        <!-- Actors Dropdown -->
                        <div class="mb-4 dropdown-container">
                            <label class="form-label d-flex justify-content-between" @click="toggleDropdown('actors')">
                                Actors
                                <span :class="{ 'rotate-180': dropdownStates.actors }" class="dropdown-arrow"><i
                                        class='bx bxs-chevron-down'></i></span>
                            </label>
                            <div v-if="dropdownStates.actors" class="dropdown-content">
                                <input type="text" id="actors" v-model="actorInput" @keydown="handleActorInput"
                                    placeholder="Enter actors (comma-separated)" class="form-control" />
                                <div class="tag-list mt-2 d-flex flex-wrap gap-2">
                                    <span v-for="actor in formData.actorsList" :key="actor" class="tag">
                                        {{ actor }}
                                        <button type="button" @click="removeActor(actor)"
                                            class="x-btn btn-close btn-close-white btn-sm"></button>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Rating Range Dropdown -->
                        <div class="mb-4 dropdown-container">
                            <label class="form-label d-flex justify-content-between"
                                @click="toggleDropdown('ratingRange')">
                                Rating Range
                                <span :class="{ 'rotate-180': dropdownStates.ratingRange }" class="dropdown-arrow"><i
                                        class='bx bxs-chevron-down'></i></span>
                            </label>
                            <div v-if="dropdownStates.ratingRange" class="dropdown-content">
                                <input type="range" min="0" max="5" v-model="formData.ratingRange[0]" step="0.05"
                                    class="form-range mb-2" />
                                <input type="range" min="0" max="5" v-model="formData.ratingRange[1]" step="0.05"
                                    class="form-range" />
                                <div class="d-flex justify-content-between text-muted">
                                    <span class="num-range">{{ formData.ratingRange[0] }} <i class='bx bx-star'></i></span>
                                    <span class="num-range">{{ formData.ratingRange[1] }} <i class='bx bx-star'></i></span>
                                </div>
                            </div>
                        </div>

                        <!-- Number of Movies Dropdown -->
                        <div class="mb-4 dropdown-container">
                            <label class="form-label d-flex justify-content-between"
                                @click="toggleDropdown('numMovies')">
                                Number of Movies
                                <span :class="{ 'rotate-180': dropdownStates.numMovies }" class="dropdown-arrow"><i
                                        class='bx bxs-chevron-down'></i></span>
                            </label>
                            <div v-if="dropdownStates.numMovies" class="dropdown-content-num-movies">
                                <input type="number" v-model="formData.numMovies" min="1" max="100" step="1"
                                    class="form-control" placeholder="Enter number of movies" />
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card-footer text-end">
                    <button type="submit" class="btn btn-primary">
                        {{ isBatchAdd ? 'Add Movies' : 'Add Movie' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import HeaderPage from '@/components/HeaderPage.vue';
import DatePicker from '@/components/DatePicker.vue';

export default {
    name: 'AddMovies',
    components: {
        HeaderPage,
        DatePicker,
    },
    data() {
        return {
            isBatchAdd: false,
            selectedGenre: '',
            genres: ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Thriller', 'Romance', 'Adventure', 'Fantasy',
                'Animation', 'Crime', 'Mystery', 'Family', 'Biography', 'History', 'War', 'Music', 'Sport', 'Western',
                'Documentary', 'Musical', 'Short', 'Adult', 'News', 'Reality-TV', 'Talk-Show', 'Game-Show', 'Film-Noir'
            ],

            formData: {
                movieName: '',
                genre: [],
                startDate: '',
                endDate: '',
                director: '',
                actorsList: [],
                ratingRange: [0, 5],
                numMovies: 1,
            },

            actorInput: '',

            dropdownStates: {
                genre: false,
                dateRange: false,
                director: false,
                actors: false,
                ratingRange: false,
                numMovies: true,
            }
        };
    },
    methods: {

        toggleDropdown(field) {
            // Toggle the selected dropdown visibility
            this.dropdownStates[field] = !this.dropdownStates[field];
        },
        addGenre() {
            if (this.selectedGenre && !this.formData.genre.includes(this.selectedGenre)) {
                this.formData.genre.push(this.selectedGenre);
            }
            this.selectedGenre = '';

        },
        removeGenre(genre) {
            this.formData.genre = this.formData.genre.filter((g) => g !== genre);
        },
        handleActorInput(event) {
            // Check if the key pressed is comma (,) or Enter key
            if (event.key === ',' || event.key === 'Enter') {
                event.preventDefault(); // Prevent default action (comma or enter insertion)
                this.addActor(this.actorInput.trim());
                this.actorInput = ''; // Clear the input after adding actor
            }
        },
        addActor(actor) {
            if (actor && !this.formData.actorsList.includes(actor)) {
                this.formData.actorsList.push(actor);
            }

        },

        removeActor(actor) {
            this.formData.actorsList = this.formData.actorsList.filter(a => a !== actor);
        },


        async handleSubmit() {
            // Simulated server action
            console.log('Form data:', this.formData);
            if (!this.isBatchAdd && !this.formData.movieName) {
                alert("Movie name is required.");
                return;
            }

            // Show success or error message based on submission outcome
            // Generate multiple movies based on the number of movies requested
            for (let i = 0; i < this.formData.numMovies; i++) {
                console.log(`Adding movie #${i + 1}`);
                // Here, you could send a POST request for each movie creation
            }

            alert(this.isBatchAdd ? "Movies added successfully" : "Movie added successfully");
        }


    }
};
</script>

<style scoped>
/* Additional Styles */
.tag {
    background-color: #28a745;
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.calendar-icon {
    font-size: 18px;
    /* Adjust size */
    color: #6c757d;
    /* Adjust color */
    cursor: pointer;
    /* Optional: make the icon clickable */
    /* Fine-tune vertical positioning */
    margin-top: 1vh;
    /* Fine adjustment to move the icon down */
}


.tag:hover {
    background-color: #218838;
}

.form-control {
    border-radius: 8px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    border: 1px solid #ddd;
    transition: border-color 0.3s ease-in-out;
}

.add-movies-page {
    height: 100vh;
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
    background-color: rgb(0, 0, 0);
    /* Light gray background */
    background-image: radial-gradient(circle, rgb(38, 218, 62) 1%, transparent 10%) !important;
    background-size: 20px 20px;
    /* Controls the size of the dots */
    background-position: center;
    background-repeat: repeat;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    color: #e0e0e0;
}

.dropdown-container {
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
    margin-bottom: 10px;
    color: #e0e0e0;
}

.dropdown-arrow {
    transition: transform 0.3s ease;
    font-size: 1.2rem;
}

.rotate-180 {
    transform: rotate(180deg);
}

.dropdown-content-genre {
    max-width: 250px;
}

.dropdown-content {
    max-width: 450px;
}

.dropdown-content-num-movies {
    max-width: 100px;
}


.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
    max-height: 6vh;
    overflow-y: auto;
}

.x-btn {
    padding: 2px;
    margin-left: 5px;
    cursor: pointer;
    height: 1vh;
}

/* Overlay */
.overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1;
}

/* Header */
.header-page {
    z-index: 2;
    width: 100%;
    color: #fff;
    text-align: center;
    padding: 20px;
    background-color: rgb(0, 0, 0);
}

/* Admin Movie Form */
#admin-movie-form {
    z-index: 20;
    max-width: 640px;
    width: 100%;
    background: rgb(32, 32, 32);
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    border-color:#3f3f3f
}


/* Form Header */
.card-header {
    background: rgb(32, 32, 32);
    color: #fff;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    padding: 20px;
    text-align: center;
}

.card-title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
}

.card-description {
    font-size: 0.9rem;
    color: #ccc;
}

/* Form Fields */
.form-label {
    font-weight: bold;
    color: #e0e0e0;
}

.form-control,
.form-select {
    border-radius: 8px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    border: 1px solid #ddd;
    transition: border-color 0.3s ease-in-out;
}

.form-control:focus,
.form-select:focus {
    border-color: #2e312f;
    outline: none;
}



/* Checkbox */
.form-check-label {
    font-size: 0.9rem;
    color: #e0e0e0;
}

/* Override Bootstrap checkbox checked color */
.form-check-input:checked {
    background-color: #28a745 !important;
    /* Custom color */
    border-color: #28a745 !important;
}

/* Genre Tag Buttons */
.genre-tag {
    color: #fff;
    border: none;
    border-radius: 20px;
    padding: 5px 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.genre-tag:hover {
    background-color: #262926;
}

/* Rating Range */
.rating-range {
    display: flex;
    justify-content: space-between;
    color: #555;
}

/* Submit Button */
.btn-primary {
    background-color: #10c00a;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.btn-primary:hover {
    background-color: #2d312d;
}

.card-body {
    padding: 1.5rem;
    max-height: 70vh;
    overflow-y: auto;
}



.card-body::-webkit-scrollbar-thumb {
    background-color: #888;
    border-radius: 10px;
}


.collapse .card-body {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}

.btn-secondary {
    text-align: left;
    padding: 0.75rem;
    font-weight: bold;
}

/* Footer */
.footer {
    background-color: #121212;
    color: #fff;
    padding: 10px;
    text-align: center;
    position: absolute;
    bottom: 0;
    width: 100%;
    z-index: 5;
    font-size: 0.85rem;
}

/* Style the circle (thumb) */
input[type="range"]::-webkit-slider-thumb {
    background-color: #28a745;
    /* Custom color for the thumb */
    border: 2px solid #28a745;
}

input[type="range"]::-moz-range-thumb {
    background-color: #28a745;
    border: 2px solid #28a745;
}

input[type="range"]::-ms-thumb {
    background-color: #28a745;
    border: 2px solid #28a745;
}

/* Genre select box hover */
select.form-select:hover {
    border-color: #28a745;
}


.form-control:hover {
    border-color: #28a745;
    /* Border color on hover */
}
.num-range {
    color: #fff;
}
</style>
