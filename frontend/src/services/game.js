import { requestBackend } from './api';

/**
 * Wrapper func - server request to get all games.
 * @returns {Promise<Object>}  
 */
export const getAllGames = async () => {
    const tokens = {
        sessionToken: localStorage.getItem("session_token"),
        // TODO: Include CSRF token
        csrfToken: localStorage.getItem("csrf_token"),
    }    
    const response = await requestBackend("GET", "admin/games", tokens, null, null);

    if (response.error) {
        throw new Error(response.error);
    }
    return response;
}

/**
 * Wrapper func - server request to set all games for the user.
 * @returns {Promise<Object>}  
 */
export const putGames = async (body) => {
    const tokens = {
        sessionToken: localStorage.getItem("session_token"),
        // TODO: Include CSRF token
        csrfToken: localStorage.getItem("csrf_token"),
    }    
    const response = await requestBackend("PUT", "admin/games", tokens, body, null);

    if (response.error) {
        throw new Error(response.error);
    }
    return response;
}

/**
 * Wrapper func - server PUT request to update game
 * @param {Object} body - this is the object with 'games' as a key
 * @returns 
 */
export const updateGame = async (body) => {
    const tokens = {
        sessionToken: localStorage.getItem("session_token"),
        // TODO: Include CSRF token
        csrfToken: localStorage.getItem("csrf_token"),
    }    
    const response = await requestBackend("PUT", "admin/games", tokens, body, null);

    if (response.error) {
        throw new Error(response.error);
    }
    return response;
}

export const postMutateGame = async (gameId, body) => {
    const tokens = {
        sessionToken: localStorage.getItem("session_token"),
        // TODO: Include CSRF token
        csrfToken: localStorage.getItem("csrf_token"),
    }    
    const response = await requestBackend("POST", `admin/game/${gameId}/mutate`, tokens, body, null);
    return response;
}

/**
 * Generates an updated version of the questions array based on the requested modification.
 * @param {String} requestType - specify type - create, update, delete
 * @param {Array} questionArr - current question array
 * @param {String} questionType - multi, single, judgment
 * @param {Object} question - question to be added, updated, or removed
 * @returns {Array} - modified question array
 */
export const generateUpdatedQuestions = (requestType, questionArr, question) => {
    let updatedQuestions = [];
    if (requestType === "create") {
        if (questionArr.length > 0) delete questionArr[questionArr.length - 1].final
        question.final = true;
        updatedQuestions = [...questionArr, question];
    } else if (requestType === "update") {
        let replaced = false;
        updatedQuestions = questionArr.map(curr => {
            delete curr.final
            if (curr.id.toString() === question.id.toString()) {
                replaced = true;
                delete question.final
                return question
            }
            return curr;
        })

        if (!replaced) {
            updatedQuestions.push(question);
        }

        updatedQuestions[updatedQuestions.length - 1].final = true
    } else {
        // delete
        updatedQuestions = questionArr.filter(currQuestion => currQuestion.id !== question.id);
        updatedQuestions.map((q) => {
            delete q.final
        })
        updatedQuestions[updatedQuestions.length - 1].final = true
    }

    return updatedQuestions;
};

/**
 * Wrapper func to handle getting a specific question from gameId and questionId from url query params
 * @param {String} gameId 
 * @param {String} questionId 
 * @returns {Array} - array of questions
 */
export const getQuestion = async (gameId, questionId) => {
    const tokens = {
        sessionToken: localStorage.getItem("session_token"),
        // TODO: Include CSRF token
        csrfToken: localStorage.getItem("csrf_token"),
    }
    const response = await requestBackend("GET", "admin/games", tokens, null, null);
    const games = response.games.find(game => game.id.toString() === gameId);

    const questions = games.questions.find(question => question.id.toString() === questionId);
    return questions;
}

/**
 * Input validation func to check if question input is valid
 * @param {String} questionType - type of question (Multi-Choice, Single-Choice, Judgement) 
 * @param {Object} question - question object to validate
 * @returns boolean - true/false
 */
export const gameInputValidation = (question) => {
    // TODO: Implement comprehensive input validation and sanitization
    let message = ""

    if (question.text.trim() === "") {
        message = "Question text cannot be empty!";
    } else if (question.summary.trim() === "") {
        message = "Description box cannot be empty!";
    } else if (question.duration <= 0) {
        message = "Question duration must be greater than 0!";
    } else if (question.points <= 0) {
        message = "Question points must be greater than 0!";
    } else if (question.type === "Multi-Choice" || question.type === "Single-Choice") {
        if (question.correctAnswers.length === 0) {
            message = "You must select at least one correct answer!"
        } else if (question.options.length === 0) {
            message = "You must add at least one option choice!";
        } else if (question.correctAnswers.length > question.options.length) {
            message = "There are more correct answers than total options!";
        } else if (question.type === "Multi-Choice" && question.correctAnswers.length <= 1) {
            message = `Question "${question.text}" is multi-choice, but only has one correct answer! 
                       Needs to have at least two correct answers.`;
        } else if (!question.correctAnswers.every(ans => question.options.includes(ans))) {
            message = `All correct answers must also be listed as options in ${question.text}! 
                       Check your JSON game file!`;
        }
    } else if (question.type === "Judgement") {
        if (!question.correctAnswers || question.correctAnswers.length === 0 ||
            question.correctAnswers[0]?.trim() === "") {
            message = "Judgement questions require a correct answer!";
        }
    }

    if (message !== "") {
        throw new Error(message)
    }
}

/**
 * Wrapper func to handle question updates (create, update, delete)
 * @param {String} requestType - specify type - create, update, delete
 * @param {Object} questionReqObj - object containing gameId, questionArr, questionObj, setQuestionArr
 * @param {Function} setAlertMessage - function to set alert message
 * @param {Function} setAlertType - Function to set alert type
 */
export const handleQuestionUpdate = async (requestType, questionReqObj, setAlertMessage, setAlertType) => {
    const { gameId, questionArr, questionObj, setQuestionArr } = questionReqObj;

    if (requestType !== "delete") {
        try {
            gameInputValidation(questionObj)
        } catch (error) {
            throw new Error(error.message)
        }
    }

    // generate updated questions array
    let updatedQuestions = []
    if (requestType === "create") {
        updatedQuestions = generateUpdatedQuestions("create", questionArr, questionObj)
        setAlertMessage("Question created successfully!");
    } else if (requestType === "update") {
        updatedQuestions = generateUpdatedQuestions("update", questionArr, questionObj)
        setAlertMessage("Question updated successfully!");
    } else {
        updatedQuestions = generateUpdatedQuestions("delete", questionArr, questionObj)
        setAlertMessage("Question deleted successfully!");
    }
    setAlertType("SUCCESS");

    // update game with new questions to backend wrapper
    try {
        const response = await getAllGames();
        const existingGames = response.games.map(game => {
            if (game.id.toString() === gameId) {
                return {
                    ...game,
                    questions: updatedQuestions
                };
            }
            return game;
        });
        let body = {
            games: existingGames
        }

        await updateGame(body);
        setQuestionArr(updatedQuestions)
    } catch (error) {
        throw new Error(error.message)
    }
}

/**
 * Helper func - format countdown time remaining
 * @param {Number} remaining 
 * @returns 
 */
export const formatCountdown = (remaining) => {
    const totalSeconds = Math.ceil(remaining / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    if (hours > 0) {
        return `${hours}h ${minutes}m ${seconds}s remaining`;
    } else if (minutes > 0) {
        return `${minutes}m ${seconds}s remaining`;
    } else {
        return `${seconds}s remaining`;
    }
}