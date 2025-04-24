// Example API integration code for CoffeeHouse

// Base URL for the API
const API_BASE_URL = "https://api.coffeehouse.com/v1";

// Function to fetch user data
async function fetchUserData(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`);
        if (!response.ok) {
            throw new Error(`Error fetching user data: ${response.statusText}`);
        }
        const data = await response.json();
        console.log("User Data:", data);
        return data;
    } catch (error) {
        console.error("Error:", error);
    }
}

// Function to create a new user
async function createUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });
        if (!response.ok) {
            throw new Error(`Error creating user: ${response.statusText}`);
        }
        const data = await response.json();
        console.log("User Created:", data);
        return data;
    } catch (error) {
        console.error("Error:", error);
    }
}

// Function to update user data
async function updateUser(userId, updatedData) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updatedData),
        });
        if (!response.ok) {
            throw new Error(`Error updating user: ${response.statusText}`);
        }
        const data = await response.json();
        console.log("User Updated:", data);
        return data;
    } catch (error) {
        console.error("Error:", error);
    }
}

// Function to delete a user
async function deleteUser(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
            method: "DELETE",
        });
        if (!response.ok) {
            throw new Error(`Error deleting user: ${response.statusText}`);
        }
        console.log(`User with ID ${userId} deleted successfully.`);
    } catch (error) {
        console.error("Error:", error);
    }
}

// Example usage
// fetchUserData(1);
// createUser({ name: "John Doe", email: "john.doe@example.com" });
// updateUser(1, { name: "Jane Doe" });
// deleteUser(1);