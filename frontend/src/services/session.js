// session.js
// Utility functions for managing game sessions, including creating sessions, session status etc.

import { requestBackend } from './api';
import { calcDuration } from '@/utils/helpers';
/**
 * Function to create a new session
 * @param {String} sessionId
 * @returns {Promise<Object>} 
 */
export const getSessionStatus = async (sessionId) => {
    const sessionToken = localStorage.getItem("session_token");
    // TODO: Retrieve CSRF token for request
    const csrfToken = localStorage.getItem("csrf_token");
    const response = await requestBackend("GET", `admin/session/${sessionId}/status`, {sessionToken, csrfToken}, null, null);

    if (response.error) {
        throw new Error(response.error);
    }
    return response;
}

/**
 * Function to get the session results 
 * @param {String} sessionId 
 * @returns {Promise<Object>}
 */
export const getSessionResults = async (sessionId) => {
    const sessionToken = localStorage.getItem("session_token");
    // TODO: Retrieve CSRF token for request
    const csrfToken = localStorage.getItem("csrf_token");
    const response = await requestBackend("GET", `admin/session/${sessionId}/results`, {sessionToken, csrfToken}, null, null);
    console.log(response)
    if (response.error) {
        throw new Error(response.error);
    }
    return response;
}

/**
 * Gets the player score based on the questions and answers
 * @param {String} questions 
 * @param {Promise<Object>} answersArr 
 * @returns 
 */
export const getPlayerScore = (questions, answersArr) => {
    let points = 0
    for (let i = 0; i < answersArr.length; i++) {
        const timeTaken = calcDuration(answersArr[i].questionStartedAt, answersArr[i].answeredAt)
        const pointsAvailable = parseInt(questions[i].points)
        points += pointsAwarded(timeTaken, answersArr[i].correct, pointsAvailable, questions[i].duration)
    }
    return points
}

/**
 * Calculates the points awarded based on the time taken, correctness, and points available
 * @param {Number} timeTaken - time taken to answer the question
 * @param {Boolean} correct - whether the answer was correct
 * @param {Number} points - points available for the question
 * @param {Number} totalDuration - total duration of the question
 * @returns 
 */
export const pointsAwarded = (timeTaken, correct, points, totalDuration) => {
    if (correct) {
        console.log(totalDuration)
        if (timeTaken < totalDuration * 0.3 * 1000) {
            timeTaken = 1
        } else {
            timeTaken = Math.E ** (-0.3 * (timeTaken / 1000 - totalDuration * 0.3))
        }
        return timeTaken * points
    }
    return 0
}
