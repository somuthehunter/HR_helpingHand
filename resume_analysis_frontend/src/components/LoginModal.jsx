import React from "react";
import { useState  } from "react";
import { Routes, useNavigate  , Route} from "react-router-dom";
import axios from 'axios';
import Dashboard from "./hr_side_dashboard/Dashboard";
const LoginModal = ({ closeModal }) => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(""); // Clear previous error messages

        try {
            const response = await axios.post("http://127.0.0.1:8000/api/login/", {
                email,
                password,
                role
            });

            const { access_token, user_name, user_id } = response.data;
            
            // Store token and user info in localStorage
            localStorage.setItem("authToken", access_token);
            localStorage.setItem("userName", user_name);
            localStorage.setItem("userId", user_id);

            console.log("Login successful:", response.data);

            // Redirect to Dashboard
            

            navigate("/dashboard");
        } catch (err) {
            if (err.response && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError("Something went wrong. Please try again.");
            }
        }
    };


    return (
        <div 
            className="fixed inset-0 flex items-center justify-center z-50 
                       bg-black bg-opacity-60 backdrop-blur-lg"
            onClick={closeModal} // Close modal when clicking outside
        >
            {/* Modal Content */}
            <div 
                className="bg-n-1/10 p-6 rounded-lg shadow-lg w-96 relative"
                onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
            >
                <h2 className="text-2xl font-bold text-center">Sign In</h2>
                <form onSubmit={handleLogin}>
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
                        Login
                    </button>
                    don't have account ? <a href="#">Sign Up</a>
                </form>
            </div>
        </div>
    );
};

export default LoginModal;
