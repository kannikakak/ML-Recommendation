// Frontend JavaScript for Recommendation System

class RecommendationApp {
    constructor() {
        this.currentTab = 'recommendations';
        this.recommendations = [];
        this.filters = {
            category: '',
            minRating: 0,
            maxRating: 5,
            province: ''
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadRecommendations();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Filter inputs
        document.getElementById('categoryFilter')?.addEventListener('change', (e) => {
            this.filters.category = e.target.value;
            this.filterRecommendations();
        });

        document.getElementById('ratingFilter')?.addEventListener('input', (e) => {
            this.filters.minRating = parseFloat(e.target.value);
            this.filterRecommendations();
        });

        document.getElementById('provinceFilter')?.addEventListener('change', (e) => {
            this.filters.province = e.target.value;
            this.filterRecommendations();
        });

        // Search functionality
        document.getElementById('searchInput')?.addEventListener('input', (e) => {
            this.searchRecommendations(e.target.value);
        });

        // Get recommendations button
        document.getElementById('getRecommendations')?.addEventListener('click', () => {
            this.getPersonalizedRecommendations();
        });
    }

    switchTab(tabName) {
        // Update active tab
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Show/hide content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });
        document.getElementById(`${tabName}-content`).style.display = 'block';

        this.currentTab = tabName;
    }

    async loadRecommendations() {
        try {
            this.showLoading(true);
            // In a real app, this would be an API call
            const response = await this.mockApiCall('/api/recommendations');
            this.recommendations = response.data;
            this.displayRecommendations(this.recommendations);
            this.showLoading(false);
        } catch (error) {
            console.error('Error loading recommendations:', error);
            this.showAlert('Error loading recommendations. Please try again.', 'error');
            this.showLoading(false);
        }
    }

    displayRecommendations(recommendations) {
        const container = document.getElementById('recommendationsGrid');
        if (!container) return;

        if (recommendations.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <h3>No recommendations found</h3>
                    <p>Try adjusting your filters or search terms.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = recommendations.map(place => `
            <div class="recommendation-card">
                <div class="recommendation-image">
                    <i class="fas fa-map-marker-alt"></i>
                    ${place.name}
                </div>
                <div class="recommendation-content">
                    <h3 class="recommendation-title">${place.name}</h3>
                    <div class="recommendation-category">${place.category}</div>
                    <p class="recommendation-description">${place.description}</p>
                    <div class="recommendation-stats">
                        <div class="rating">
                            <div class="stars">${this.generateStars(place.rating)}</div>
                            <span>${place.rating}/5</span>
                        </div>
                        <div class="reviews-count">${place.reviews} reviews</div>
                    </div>
                    <div style="margin-top: 15px;">
                        <button class="btn btn-primary" onclick="app.viewDetails('${place.id}')">
                            View Details
                        </button>
                        <button class="btn btn-secondary" onclick="app.addToFavorites('${place.id}')">
                            <i class="fas fa-heart"></i> Save
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

        let starsHTML = '';
        for (let i = 0; i < fullStars; i++) {
            starsHTML += '<i class="fas fa-star"></i>';
        }
        if (hasHalfStar) {
            starsHTML += '<i class="fas fa-star-half-alt"></i>';
        }
        for (let i = 0; i < emptyStars; i++) {
            starsHTML += '<i class="far fa-star"></i>';
        }
        return starsHTML;
    }

    filterRecommendations() {
        const filtered = this.recommendations.filter(place => {
            const categoryMatch = !this.filters.category || place.category === this.filters.category;
            const ratingMatch = place.rating >= this.filters.minRating && place.rating <= this.filters.maxRating;
            const provinceMatch = !this.filters.province || place.province === this.filters.province;
            
            return categoryMatch && ratingMatch && provinceMatch;
        });

        this.displayRecommendations(filtered);
    }

    searchRecommendations(query) {
        if (!query.trim()) {
            this.displayRecommendations(this.recommendations);
            return;
        }

        const filtered = this.recommendations.filter(place => 
            place.name.toLowerCase().includes(query.toLowerCase()) ||
            place.description.toLowerCase().includes(query.toLowerCase()) ||
            place.category.toLowerCase().includes(query.toLowerCase())
        );

        this.displayRecommendations(filtered);
    }

    async getPersonalizedRecommendations() {
        const preferences = this.getUserPreferences();
        
        try {
            this.showLoading(true);
            // In a real app, this would send preferences to the backend
            const response = await this.mockApiCall('/api/personalized-recommendations', preferences);
            this.recommendations = response.data;
            this.displayRecommendations(this.recommendations);
            this.showAlert('Personalized recommendations updated!', 'success');
            this.showLoading(false);
        } catch (error) {
            console.error('Error getting personalized recommendations:', error);
            this.showAlert('Error getting recommendations. Please try again.', 'error');
            this.showLoading(false);
        }
    }

    getUserPreferences() {
        return {
            category: document.getElementById('preferredCategory')?.value || '',
            budget: document.getElementById('budget')?.value || '',
            travelStyle: document.getElementById('travelStyle')?.value || '',
            interests: Array.from(document.querySelectorAll('input[name="interests"]:checked')).map(cb => cb.value)
        };
    }

    viewDetails(placeId) {
        // Show detailed view of the place
        const place = this.recommendations.find(p => p.id === placeId);
        if (place) {
            this.showPlaceModal(place);
        }
    }

    addToFavorites(placeId) {
        // Add place to favorites
        const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        if (!favorites.includes(placeId)) {
            favorites.push(placeId);
            localStorage.setItem('favorites', JSON.stringify(favorites));
            this.showAlert('Added to favorites!', 'success');
        } else {
            this.showAlert('Already in favorites!', 'warning');
        }
    }

    showPlaceModal(place) {
        // Create and show modal with place details
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
                <h2>${place.name}</h2>
                <div class="modal-body">
                    <p><strong>Category:</strong> ${place.category}</p>
                    <p><strong>Rating:</strong> ${place.rating}/5 (${place.reviews} reviews)</p>
                    <p><strong>Description:</strong> ${place.description}</p>
                    <p><strong>Location:</strong> ${place.province || 'N/A'}</p>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary" onclick="app.getDirections('${place.id}')">
                        Get Directions
                    </button>
                    <button class="btn btn-secondary" onclick="this.parentElement.parentElement.parentElement.remove()">
                        Close
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    getDirections(placeId) {
        // Open directions in a new tab (Google Maps)
        const place = this.recommendations.find(p => p.id === placeId);
        if (place && place.coordinates) {
            const url = `https://www.google.com/maps/dir/?api=1&destination=${place.coordinates.lat},${place.coordinates.lng}`;
            window.open(url, '_blank');
        } else {
            this.showAlert('Directions not available for this location.', 'warning');
        }
    }

    showLoading(show) {
        const loader = document.getElementById('loadingSpinner');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
    }

    showAlert(message, type = 'success') {
        const alertContainer = document.getElementById('alertContainer') || this.createAlertContainer();
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            ${message}
            <button style="float: right; background: none; border: none; font-size: 18px; cursor: pointer;" onclick="this.parentElement.remove()">×</button>
        `;
        
        alertContainer.appendChild(alert);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 5000);
    }

    createAlertContainer() {
        const container = document.createElement('div');
        container.id = 'alertContainer';
        container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1000; min-width: 300px;';
        document.body.appendChild(container);
        return container;
    }

    // Mock API call for demo purposes
    async mockApiCall(endpoint, data = null) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    data: this.getMockData(endpoint)
                });
            }, 1000);
        });
    }

    getMockData(endpoint) {
        const mockData = {
            '/api/recommendations': [
                {
                    id: '1',
                    name: 'Royal Palace of Cambodia',
                    category: 'Tourist Attraction',
                    rating: 4.3,
                    reviews: 12506,
                    description: 'Royal Palace of Cambodia is a popular tourist attraction located in Phnom Penh. It is known for its cultural significance and attracts many visitors each year.',
                    province: 'Phnom Penh',
                    coordinates: { lat: 11.563877, lng: 104.9312521 }
                },
                {
                    id: '2',
                    name: 'Tuol Sleng Genocide Museum',
                    category: 'Tourist Attraction',
                    rating: 4.6,
                    reviews: 11655,
                    description: 'Tuol Sleng Genocide Museum is a popular tourist attraction located in Phnom Penh. It is known for its cultural significance and attracts many visitors each year.',
                    province: 'Phnom Penh',
                    coordinates: { lat: 11.548851, lng: 104.9176751 }
                },
                {
                    id: '3',
                    name: 'Wat Phnom Daun Penh',
                    category: 'Tourist Attraction',
                    rating: 4.4,
                    reviews: 8646,
                    description: 'Wat Phnom Daun Penh is a popular tourist attraction located in Phnom Penh. It is known for its cultural significance and attracts many visitors each year.',
                    province: 'Phnom Penh',
                    coordinates: { lat: 11.5761478, lng: 104.9230936 }
                }
            ],
            '/api/personalized-recommendations': [
                {
                    id: '4',
                    name: 'National Museum of Cambodia',
                    category: 'Tourist Attraction',
                    rating: 4.1,
                    reviews: 6478,
                    description: 'National Museum of Cambodia is a popular tourist attraction located in Phnom Penh. It is known for its cultural significance and attracts many visitors each year.',
                    province: 'Phnom Penh',
                    coordinates: { lat: 11.5658543, lng: 104.9291464 }
                }
            ]
        };

        return mockData[endpoint] || mockData['/api/recommendations'];
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new RecommendationApp();
});

// Additional utility functions
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const isVisible = section.style.display !== 'none';
    section.style.display = isVisible ? 'none' : 'block';
}

function resetFilters() {
    document.getElementById('categoryFilter').value = '';
    document.getElementById('ratingFilter').value = 0;
    document.getElementById('provinceFilter').value = '';
    document.getElementById('searchInput').value = '';
    
    if (window.app) {
        window.app.filters = {
            category: '',
            minRating: 0,
            maxRating: 5,
            province: ''
        };
        window.app.loadRecommendations();
    }
}