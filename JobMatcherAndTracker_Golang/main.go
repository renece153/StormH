package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

// OpenAI API Key
const openAIAPIKey = "API KEY"

// Job structure to hold job listing information
type Job struct {
	Title         string `json:"title"`
	Description   string `json:"description"`
	HumanResource string `json:"hrEmail"`
}

// User structure for job experience and skills
type User struct {
	Experience string `json:"experience"`
	Skills     string `json:"skills"`
}

// Response structure to hold the matching jobs
type MatchResult struct {
	Title         string `json:"title"`
	HumanResource string `json:"hrEmail"`
}

// OpenAI Response structure for extracted information
type OpenAIResponse struct {
	Choices []struct {
		Text string `json:"text"`
	} `json:"choices"`
}

func main() {
	http.HandleFunc("/match", matchHandler)
	http.HandleFunc("/jobs", jobsHandler)
	http.ListenAndServe(":8080", nil)
}

// Handler to list matched jobs
func matchHandler(w http.ResponseWriter, r *http.Request) {
	// Read the request body
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Unable to read request body", http.StatusBadRequest)
		return
	}

	// Parse the User input
	var user User
	err = json.Unmarshal(body, &user)
	if err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	// Simulated database jobs
	jobs := getDatabaseJobs()

	// OpenAI prompt to find matching jobs
	prompt := fmt.Sprintf("From the following experience and skills, identify jobs that match:\nExperience: %s\nSkills: %s\n\nJobs:\n%s",
		user.Experience, user.Skills, jobsToString(jobs))

	// Call OpenAI to process the prompt
	openAIResponse := callOpenAI(prompt)
	matchedJobs := extractMatchedJobs(openAIResponse.Choices[0].Text, jobs)
	response, _ := json.Marshal(matchedJobs)
	w.Header().Set("Content-Type", "application/json")
	w.Write(response)
}

// Handler to list all job listings (for displaying the job tracker)
func jobsHandler(w http.ResponseWriter, r *http.Request) {
	jobs := getDatabaseJobs()
	response, _ := json.Marshal(jobs)
	w.Header().Set("Content-Type", "application/json")
	w.Write(response)
}

// Simulated database function to get jobs
func getDatabaseJobs() []Job {
	return []Job{
		{"Backend Developer", "Develop REST APIs", "hr@techcorp.com"},
		{"Frontend Developer", "Develop React applications", "hr@webcorp.com"},
		{"DevOps Engineer", "Manage CI/CD pipelines", "hr@cloudservice.com"},
	}
}

// Function to format job listings into a string
func jobsToString(jobs []Job) string {
	var formattedJobs string
	for _, job := range jobs {
		formattedJobs += fmt.Sprintf("Title: %s\nDescription: %s\n\n", job.Title, job.Description)
	}
	return formattedJobs
}

// Function to extract matched jobs from the response
func extractMatchedJobs(responseText string, jobs []Job) []MatchResult {
	var matches []MatchResult
	for _, job := range jobs {
		if strings.Contains(strings.ToLower(responseText), strings.ToLower(job.Title)) {
			matches = append(matches, MatchResult{Title: job.Title, HumanResource: job.HumanResource})
		}
	}
	return matches
}

// Function to call OpenAI API
func callOpenAI(prompt string) OpenAIResponse {
	reqBody := map[string]interface{}{
		"model":      "text-davinci-003",
		"prompt":     prompt,
		"max_tokens": 200,
	}
	jsonReq, _ := json.Marshal(reqBody)
	req, _ := http.NewRequest("POST", "https://api.openai.com/v1/completions", bytes.NewBuffer(jsonReq))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+openAIAPIKey)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
		return OpenAIResponse{}
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	var openAIResponse OpenAIResponse
	json.Unmarshal(body, &openAIResponse)

	return openAIResponse
}
