// Reusable UI Components

class UIComponents {
    
    // Header Component
    static createHeader(title, subtitle) {
        return `
            <div class="header">
                <h1>${title}</h1>
                <p>${subtitle}</p>
            </div>
        `;
    }

    // Navigation Tabs Component
    static createNavTabs(tabs) {
        const tabsHTML = tabs.map(tab => `
            <button class="nav-tab ${tab.active ? 'active' : ''}" data-tab="${tab.id}">
                ${tab.icon ? `<i class="${tab.icon}"></i>` : ''} ${tab.label}
            </button>
        `).join('');

        return `
            <div class="nav-tabs">
                ${tabsHTML}
            </div>
        `;
    }

    // Search Component
    static createSearchComponent(placeholder = "Search places...") {
        return `
            <div class="form-group">
                <div style="position: relative;">
                    <input type="text" id="searchInput" class="form-input" 
                           placeholder="${placeholder}" style="padding-left: 45px;">
                    <i class="fas fa-search" style="position: absolute; left: 15px; top: 50%; 
                       transform: translateY(-50%); color: #9ca3af;"></i>
                </div>
            </div>
        `;
    }

    // Filter Component
    static createFilterComponent() {
        return `
            <div class="filters">
                <h3 style="margin-bottom: 20px; color: var(--text-primary);">
                    <i class="fas fa-filter"></i> Filters
                </h3>
                <div class="filter-grid">
                    <div class="form-group">
                        <label class="form-label">Category</label>
                        <select id="categoryFilter" class="form-select">
                            <option value="">All Categories</option>
                            <option value="Tourist Attraction">Tourist Attraction</option>
                            <option value="Restaurant">Restaurant</option>
                            <option value="Hotel">Hotel</option>
                            <option value="Shopping">Shopping</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Minimum Rating</label>
                        <input type="range" id="ratingFilter" class="form-input" 
                               min="0" max="5" step="0.1" value="0">
                        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: var(--text-secondary);">
                            <span>0</span><span>2.5</span><span>5</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Province</label>
                        <select id="provinceFilter" class="form-select">
                            <option value="">All Provinces</option>
                            <option value="Phnom Penh">Phnom Penh</option>
                            <option value="Siem Reap">Siem Reap</option>
                            <option value="Battambang">Battambang</option>
                        </select>
                    </div>
                    <div class="form-group" style="display: flex; align-items: end;">
                        <button class="btn btn-secondary" onclick="resetFilters()" style="width: 100%;">
                            <i class="fas fa-undo"></i> Reset Filters
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Preference Form Component
    static createPreferenceForm() {
        return `
            <div class="card">
                <h3 style="margin-bottom: 20px; color: var(--text-primary);">
                    <i class="fas fa-user-cog"></i> Your Preferences
                </h3>
                <div class="filter-grid">
                    <div class="form-group">
                        <label class="form-label">Preferred Category</label>
                        <select id="preferredCategory" class="form-select">
                            <option value="">No Preference</option>
                            <option value="Tourist Attraction">Tourist Attractions</option>
                            <option value="Restaurant">Restaurants</option>
                            <option value="Hotel">Hotels</option>
                            <option value="Shopping">Shopping</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Budget Range</label>
                        <select id="budget" class="form-select">
                            <option value="">Any Budget</option>
                            <option value="low">Budget-Friendly ($)</option>
                            <option value="medium">Mid-Range ($$)</option>
                            <option value="high">Luxury ($$$)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Travel Style</label>
                        <select id="travelStyle" class="form-select">
                            <option value="">Any Style</option>
                            <option value="adventure">Adventure</option>
                            <option value="relaxation">Relaxation</option>
                            <option value="cultural">Cultural</option>
                            <option value="family">Family-Friendly</option>
                        </select>
                    </div>
                </div>
                <div style="margin-top: 20px;">
                    <label class="form-label">Interests (Select all that apply)</label>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-top: 10px;">
                        ${this.createCheckboxGroup([
                            { value: 'history', label: 'History' },
                            { value: 'nature', label: 'Nature' },
                            { value: 'food', label: 'Food & Dining' },
                            { value: 'art', label: 'Art & Culture' },
                            { value: 'nightlife', label: 'Nightlife' },
                            { value: 'shopping', label: 'Shopping' }
                        ])}
                    </div>
                </div>
                <button id="getRecommendations" class="btn btn-primary" style="width: 100%; margin-top: 25px;">
                    <i class="fas fa-magic"></i> Get Personalized Recommendations
                </button>
            </div>
        `;
    }

    // Checkbox Group Helper
    static createCheckboxGroup(options) {
        return options.map(option => `
            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                <input type="checkbox" name="interests" value="${option.value}" 
                       style="margin: 0; accent-color: var(--primary-color);">
                <span style="font-size: 0.9rem;">${option.label}</span>
            </label>
        `).join('');
    }

    // Loading Spinner Component
    static createLoadingSpinner() {
        return `
            <div id="loadingSpinner" style="display: none; text-align: center; padding: 40px;">
                <div class="loading"></div>
                <p style="margin-top: 15px; color: var(--text-secondary);">Loading recommendations...</p>
            </div>
        `;
    }

    // Empty State Component
    static createEmptyState(title, message, actionButton = null) {
        return `
            <div class="empty-state" style="text-align: center; padding: 60px 20px; color: var(--text-secondary);">
                <i class="fas fa-search" style="font-size: 3rem; margin-bottom: 20px; opacity: 0.5;"></i>
                <h3 style="margin-bottom: 10px; color: var(--text-primary);">${title}</h3>
                <p style="margin-bottom: 20px; max-width: 400px; margin-left: auto; margin-right: auto;">${message}</p>
                ${actionButton ? `<button class="btn btn-primary" onclick="${actionButton.onclick}">${actionButton.text}</button>` : ''}
            </div>
        `;
    }

    // Statistics Cards Component
    static createStatsCards(stats) {
        return `
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
                ${stats.map(stat => `
                    <div class="card" style="text-align: center; padding: 20px;">
                        <div style="font-size: 2.5rem; color: var(--primary-color); margin-bottom: 10px;">
                            <i class="${stat.icon}"></i>
                        </div>
                        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 5px;">
                            ${stat.value}
                        </div>
                        <div style="color: var(--text-secondary); font-size: 0.9rem;">
                            ${stat.label}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // Map Component Placeholder
    static createMapComponent() {
        return `
            <div class="map-container">
                <div style="display: flex; align-items: center; justify-content: center; height: 100%; 
                            background: linear-gradient(135deg, #667eea, #764ba2); color: white; font-size: 1.2rem;">
                    <div style="text-align: center;">
                        <i class="fas fa-map-marked-alt" style="font-size: 3rem; margin-bottom: 15px;"></i>
                        <div>Interactive Map</div>
                        <div style="font-size: 0.9rem; opacity: 0.8; margin-top: 5px;">
                            Map integration coming soon
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Modal Component
    static createModal(id, title, content, footer = '') {
        return `
            <div id="${id}" class="modal" style="display: none; position: fixed; z-index: 1000; left: 0; top: 0; 
                 width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);">
                <div class="modal-content" style="background: white; margin: 5% auto; padding: 0; width: 90%; max-width: 600px; 
                     border-radius: 16px; box-shadow: var(--shadow-lg); animation: modalSlideIn 0.3s;">
                    <div class="modal-header" style="padding: 20px 30px; border-bottom: 1px solid var(--border-color); 
                         display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: var(--text-primary);">${title}</h3>
                        <span class="close" style="font-size: 28px; font-weight: bold; cursor: pointer; 
                              color: var(--text-secondary);" onclick="document.getElementById('${id}').style.display='none'">&times;</span>
                    </div>
                    <div class="modal-body" style="padding: 30px;">
                        ${content}
                    </div>
                    ${footer ? `<div class="modal-footer" style="padding: 20px 30px; border-top: 1px solid var(--border-color); text-align: right;">${footer}</div>` : ''}
                </div>
            </div>
            <style>
                @keyframes modalSlideIn {
                    from { transform: translateY(-50px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
            </style>
        `;
    }

    // Reviews Component
    static createReviewsSection(reviews) {
        return `
            <div class="reviews-section" style="margin-top: 30px;">
                <h3 style="margin-bottom: 20px; color: var(--text-primary);">
                    <i class="fas fa-star"></i> Recent Reviews
                </h3>
                ${reviews.length === 0 ? 
                    this.createEmptyState('No Reviews Yet', 'Be the first to leave a review!') :
                    reviews.map(review => `
                        <div style="background: #f8fafc; border-radius: 12px; padding: 20px; margin-bottom: 15px;">
                            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                                <div>
                                    <strong style="color: var(--text-primary);">${review.userName}</strong>
                                    <div style="color: #ffd700; margin: 5px 0;">
                                        ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}
                                    </div>
                                </div>
                                <small style="color: var(--text-secondary);">${review.date}</small>
                            </div>
                            <p style="color: var(--text-secondary); line-height: 1.6; margin: 0;">${review.comment}</p>
                        </div>
                    `).join('')
                }
            </div>
        `;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIComponents;
}