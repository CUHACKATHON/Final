/**
 * Token-based Authentication Utility
 * Handles JWT token storage, retrieval, and API requests
 */

const Auth = {
    // Storage keys
    ACCESS_TOKEN_KEY: 'access_token',
    REFRESH_TOKEN_KEY: 'refresh_token',
    USER_DATA_KEY: 'user_data',

    /**
     * Store tokens in localStorage
     */
    setTokens(accessToken, refreshToken, userData = null) {
        localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken);
        localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
        if (userData) {
            localStorage.setItem(this.USER_DATA_KEY, JSON.stringify(userData));
        }
    },

    /**
     * Get access token from localStorage
     */
    getAccessToken() {
        return localStorage.getItem(this.ACCESS_TOKEN_KEY);
    },

    /**
     * Get refresh token from localStorage
     */
    getRefreshToken() {
        return localStorage.getItem(this.REFRESH_TOKEN_KEY);
    },

    /**
     * Get user data from localStorage
     */
    getUserData() {
        const userData = localStorage.getItem(this.USER_DATA_KEY);
        return userData ? JSON.parse(userData) : null;
    },

    /**
     * Clear all tokens and user data
     */
    clearTokens() {
        localStorage.removeItem(this.ACCESS_TOKEN_KEY);
        localStorage.removeItem(this.REFRESH_TOKEN_KEY);
        localStorage.removeItem(this.USER_DATA_KEY);
    },

    /**
     * Check if user is authenticated (has valid token)
     */
    isAuthenticated() {
        return !!this.getAccessToken();
    },

    /**
     * Get authorization header for API requests
     */
    getAuthHeader() {
        const token = this.getAccessToken();
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    },

    /**
     * Make authenticated fetch request with token
     */
    async authenticatedFetch(url, options = {}) {
        const token = this.getAccessToken();
        if (!token) {
            throw new Error('No access token available');
        }

        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers
        };

        const response = await fetch(url, {
            ...options,
            headers
        });

        // If token expired, try to refresh
        if (response.status === 401) {
            const refreshed = await this.refreshToken();
            if (refreshed) {
                // Retry the request with new token
                headers['Authorization'] = `Bearer ${this.getAccessToken()}`;
                return fetch(url, {
                    ...options,
                    headers
                });
            } else {
                // Refresh failed, redirect to login
                this.clearTokens();
                window.location.href = '/login/';
                throw new Error('Authentication failed');
            }
        }

        return response;
    },

    /**
     * Refresh access token using refresh token
     */
    async refreshToken() {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) {
            return false;
        }

        try {
            const response = await fetch('/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.setTokens(data.access, refreshToken); // Keep same refresh token
                return true;
            } else {
                this.clearTokens();
                return false;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
            this.clearTokens();
            return false;
        }
    },

    /**
     * Login with username and password
     */
    async login(username, password) {
        try {
            const response = await fetch('/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Store tokens
                this.setTokens(data.access, data.refresh, data.user);
                // Convert redirect URL name to actual path
                let redirectPath = '/';
                if (data.redirect === 'core:dashboard') {
                    redirectPath = '/dashboard/';
                } else if (data.redirect === 'core:index') {
                    redirectPath = '/';
                }
                return {
                    success: true,
                    user: data.user,
                    redirect: data.redirect,
                    redirectPath: redirectPath
                };
            } else {
                return {
                    success: false,
                    error: data.error || 'Login failed'
                };
            }
        } catch (error) {
            return {
                success: false,
                error: 'Connection error. Please try again.'
            };
        }
    },

    /**
     * Logout and clear tokens
     */
    async logout() {
        const refreshToken = this.getRefreshToken();
        
        try {
            // Call logout API if token exists
            if (refreshToken) {
                await fetch('/api/auth/logout/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        refresh_token: refreshToken
                    })
                });
            }
        } catch (error) {
            console.error('Logout API call failed:', error);
        } finally {
            // Always clear local tokens
            this.clearTokens();
        }
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Auth;
}

