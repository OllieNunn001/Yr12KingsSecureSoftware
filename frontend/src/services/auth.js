// auth.js
import { requestBackend } from './api';

/**
 * Wrapper func - server request to register user - setting token in browser.  
 * @param {String} email 
 * @param {String} password 
 * @param {String} name 
 * @returns {Promise<Object>}  
 */
export const adminAuthRegister = async (email, password, name) => {
    const body = { email, password, name };
    const response = await requestBackend("POST", "admin/auth/register", null, body, null);

    if (response.error) {
        throw new Error(response.error);
    }
    sessionStorage.setItem("session_token", response.session_token);
    // TODO: Store CSRF token in secure storage (sessionStorage recommended)
    sessionStorage.setItem("owner", email);
    return response;
};

/**
 * Wrapper func - server request to login user - also token set in browser.
 * @param {String} email 
 * @param {String} password 
 * @returns {Promise<Object>}  
 */

export const adminAuthLogin = async (email, password) => {
    const body = { email, password };
    const response = await requestBackend("POST", "admin/auth/login", null, body, null);

    if (response.error) {
        throw new Error(response.error);
    }
    sessionStorage.setItem("session_token", response.session_token);
    // TODO: Store CSRF token in secure storage (sessionStorage recommended)
    sessionStorage.setItem("owner", email);
    return response;
}

/**
 * Wrapper func - server request to logout user - removing token and owner from browser storage.
 */
export const adminAuthLogout = async () => {
    // const sessionToken = sessionStorage.getItem("session_token");
    // const csrfToken = sessionStorage.getItem("csrf_token");
    const tokens = {
        sessionToken: sessionStorage.getItem("session_token"),
        // TODO: Retrieve CSRF token for logout request
    }
    const ownerEmailAddress = sessionStorage.getItem("owner");

    if (!tokens || !ownerEmailAddress) {
        throw new Error("Cannot logout - no tokens or owner email found");
    }

    const response = await requestBackend("POST", "admin/auth/logout", tokens, null, null);
    if (response.error) {
        throw new Error(response.error);
    }

    sessionStorage.removeItem("session_token");
    sessionStorage.removeItem("owner");
}

/**
 * Wrapper func - server request to check if token is valid.
 * @returns {Boolean} - true if token is valid, false otherwise
 */
export const validateUserToken = async () => {
    const tokens = {
        sessionToken: sessionStorage.getItem("session_token"),
        // TODO: Include CSRF token for validation
    }
    
    // TODO: Implement proper token validation
    // using admin/games endpoint to check if token is valid as there is no endpoint to check token validity
    const response = await requestBackend("GET", "admin/games", tokens, null, null);
    if (response.error) {
        return false
    }
    return true;
}