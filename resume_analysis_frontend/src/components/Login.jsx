import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Login = () => {
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
            // navigate("/dashboard");
        } catch (err) {
            if (err.response && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError("Something went wrong. Please try again.");
            }
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="bg-n-1/10 backdrop-blur p-8 rounded shadow-md w-96">
                <h2 className="text-2xl font-semibold mb-4">Login</h2>
                {error && <p className="text-red-500">{error}</p>}
                <form onSubmit={handleLogin}>
                    <div className="mb-4">
                        <label className="block text-gray-700">Email</label>
                        <input
                            type="email"
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-gray-700">Password</label>
                        <input
                            type="password"
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-gray-700">Role</label>
                        <input
                            type="text" // FIX: Change from "password" to "text"
                            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
                    >
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
