import joblib 
from sklearn.preprocessing import LabelEncoder




gender_encoder = LabelEncoder().fit(["Female", "Male", "Other"])
academic_performance_encoder = LabelEncoder().fit(["Average", "Excellent", "Good", "Poor"])
english_proficiency_encoder = LabelEncoder().fit(["Advanced", "Basic", "Intermediate"])
github_profile_encoder = LabelEncoder().fit(["No", "Yes"])
leadership_experience_encoder = LabelEncoder().fit(["No", "Yes"])
major_encoder = LabelEncoder().fit([
	"Artificial Intelligence",
	"Business Analytics",
	"Computer Science",
	"Cybersecurity",
	"Data Science",
	"Electrical Engineering",
	"Information Technology",
	"Software Engineering",
])
university_year_encoder = LabelEncoder().fit(["Freshman", "Junior", "Senior", "Sophomore"])
linkedin_profile_encoder = LabelEncoder().fit(["No", "Yes"])
