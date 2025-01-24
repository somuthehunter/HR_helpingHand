import React, { useState } from "react";
import axios from "axios";

const SignUpModal = ({ closeModal }) => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    const handleSignUp = async (e) => {
        e.preventDefault();
        setError("");
        setMessage("");

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/register/", {
                name,
                email,
                password,
                role
            });

            console.log("Sign-Up successful:", response.data);
            setMessage("Sign Up Successfull !! redirecting...")
            closeModal(); // Close the modal after successful sign-up
        } catch (err) {
            console.error("Sign-Up error:", err);
            setError(err.response?.data?.error || "Something went wrong.");
        }
    };

    return (
        <div 
            className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-60 backdrop-blur-lg"
            onClick={closeModal}
        >
            <div 
                className="bg-n-1/10 p-6 rounded-lg shadow-lg w-96 relative"
                onClick={(e) => e.stopPropagation()}
            >
                <h2 className="text-2xl font-bold text-center mb-2">Sign Up</h2>
                {error && <p className="text-red-500 text-center">{error}</p>}
                <form onSubmit={handleSignUp}>
                    <div className="mb-4">
                        <label className="block text-n-1">Name</label>
                        <input
                            type="text"
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-n-1">Email</label>
                        <input
                            type="email"
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-n-1">Password</label>
                        <input
                            type="password"
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-n-1">Role</label>
                        <select
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            required
                        >
                            <option value="">Select your role</option>
                            <option value="HR">HR</option>
                            <option value="Student">Student</option>
                        </select>
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
                    >
                        Sign Up
                    </button>
                </form>
            </div>
        </div>
    );
};

export default SignUpModal;
