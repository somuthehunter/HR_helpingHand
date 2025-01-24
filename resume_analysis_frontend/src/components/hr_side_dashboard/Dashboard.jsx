import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../Button";

const Dashboard = () => {
    const navigate = useNavigate();

    // Get user details from localStorage
    const userName = localStorage.getItem("userName") || "User";

    const handleLogout = () => {
        localStorage.removeItem("authToken");
        localStorage.removeItem("userName");
        navigate("/login");
    };

    const [selectedOption, setSelectedOption] = useState("");
    const [resumeFile, setResumeFile] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [summary, setSummary] = useState("");
    const [jdMatch, setJdMatch] = useState("");
    const [missingKeywords, setMissingKeywords] = useState([]);
    const [profileSummary, setProfileSummary] = useState("");

    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
    };

    const handleFileChange = (event) => {
        setResumeFile(event.target.files[0]);
    };

    const handleJobDescriptionChange = (event) => {
        setJobDescription(event.target.value);
    };

const handleSubmit = async (event) => {
    event.preventDefault();

    if (!resumeFile) {
        alert("Please upload a resume.");
        return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("analysis_type", selectedOption);
    formData.append("job_description", jobDescription);

    const token = localStorage.getItem("authToken");

    try {
        const response = await fetch("http://127.0.0.1:8000/api/analysis/", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
            body: formData,
        });

        const data = await response.json();
        console.log("API Response:", data); // Debugging

        if (response.ok) {
            setSummary(data)
        } else {
            alert(data.error || "Something went wrong");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error connecting to the server.");
    }
};



    return (
        <div className="h-screen bg-black text-white">
            {/* Top Navigation Bar */}
            <div className="flex bg-gray-900 mb-5 border-b border-gray-700 p-4 shadow-md">
                <nav className="flex h-16 w-full px-6 justify-between items-center">
                    <h4 className="text-lg font-semibold">Welcome, {userName}!</h4>
                    <Button white onClick={handleLogout}>Log Out</Button>
                </nav>
            </div>

            {/* Main Content */}
            <div className="flex px-10 py-6">
                {/* Left Section (File Upload & Text Area) */}
                <div className="w-1/2 bg-gray-800 p-6 shadow-md rounded-lg">
                    <h2 className="text-xl font-semibold mb-4">Upload Resume</h2>
                    <input 
                        type="file" 
                        className="w-full p-2 border border-gray-600 rounded-lg bg-gray-700 text-white mb-4"
                        onChange={handleFileChange}
                    />
                    
                    <div className="mt-4 mb-5">
                        <h2 className="text-xl font-semibold mb-2">Select an Option</h2>
                        <select 
                            value={selectedOption} 
                            onChange={handleOptionChange} 
                            className="w-full p-2 border border-gray-600 rounded-lg bg-gray-700 text-white"
                        >
                            <option value="">Choose an option</option>
                            <option value="resume_analysis">Resume Analysis</option>
                            <option value="missing_skills">Missing Skills Analysis</option>
                        </select>
                    </div>
                    
                    <h2 className="text-xl font-semibold mb-2">Enter Job Description</h2>
                    <textarea 
                        className="w-full p-3 border border-gray-600 rounded-lg h-40 bg-gray-700 text-white mb-4"
                        placeholder="Enter job description..."
                        value={jobDescription}
                        onChange={handleJobDescriptionChange}
                    ></textarea>

                    <Button onClick={handleSubmit}>Analyze Resume</Button>
                </div>

                {/* Right Section (Summarize Resumes) */}
                 <div className="w-1/2 ml-10 bg-gray-800 p-6 shadow-md rounded-lg">
                    <h2 className="text-xl font-semibold">Summary</h2>
                   
                    <div className="mt-4 p-4 border border-gray-600 rounded-lg h-[90%] bg-gray-700">
                        Your Result is : { summary }
                       
                        
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
