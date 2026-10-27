const form = document.querySelector('#prediction-form');
const fields = [...form.querySelectorAll('[name]')];
const numericFields = new Set([
  'Age', 'Attendance_Percentage', 'Study_Hours_Per_Week', 'CGPA',
  'Programming_Skill', 'Projects_Completed', 'Certifications', 'Hackathons',
  'Internships', 'Resume_Score', 'Communication_Skills', 'Teamwork',
  'Problem_Solving', 'Interview_Score', 'Employability_Score',
]);
const decimalFields = new Set(['CGPA', 'Employability_Score']);
const sample = {
  Age: 22, Gender: 'Male', University_Year: 'Sophomore', Major: 'Computer Science',
  Attendance_Percentage: 86, Study_Hours_Per_Week: 21, CGPA: 3.28,
  Academic_Performance: 'Good', Programming_Skill: 9, Projects_Completed: 10,
  Certifications: 1, Hackathons: 6, GitHub_Profile: 'Yes', Internships: 5,
  Leadership_Experience: 'No', LinkedIn_Profile: 'No', Resume_Score: 100,
  Communication_Skills: 9, Teamwork: 7, Problem_Solving: 8,
  English_Proficiency: 'Advanced', Interview_Score: 72, Employability_Score: 231.7,
};

const resultCard = document.querySelector('.result-card');
const resultTitle = document.querySelector('#result-title');
const resultCopy = document.querySelector('#result-copy');
const resultValue = document.querySelector('#result-value');
const submitButton = document.querySelector('#submit-button');

function updateProgress() {
  const complete = fields.filter((field) => field.value.trim() !== '').length;
  document.querySelector('#progress-label').textContent = `${complete} / ${fields.length} complete`;
  document.querySelector('#progress-bar').style.width = `${(complete / fields.length) * 100}%`;
}

fields.forEach((field) => field.addEventListener('input', updateProgress));
fields.forEach((field) => field.addEventListener('change', updateProgress));

document.querySelector('#sample-button').addEventListener('click', () => {
  for (const field of fields) field.value = sample[field.name];
  updateProgress();
});

document.querySelectorAll('input[name="model"]').forEach((input) => {
  input.addEventListener('change', () => {
    document.querySelector('#result-model').textContent = input.value === 'knn_model' ? 'K-nearest neighbors' : 'Naive Bayes';
  });
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  document.querySelector('#form-error')?.remove();
  if (!document.querySelector('#api-key').reportValidity()) return;
  if (!form.reportValidity()) return;

  const payload = Object.fromEntries(fields.map((field) => {
    if (!numericFields.has(field.name)) return [field.name, field.value];
    return [field.name, decimalFields.has(field.name) ? Number.parseFloat(field.value) : Number.parseInt(field.value, 10)];
  }));
  const model = document.querySelector('input[name="model"]:checked').value;
  submitButton.disabled = true;
  submitButton.querySelector('span:first-child').textContent = 'Generating…';
  resultCard.classList.remove('is-error', 'is-not-placed', 'has-result');
  resultValue.textContent = '…';
  resultTitle.innerHTML = 'Working on<br />your forecast.';
  resultCopy.textContent = 'Your profile is being evaluated by the selected model.';

  try {
    const response = await fetch(`/predict?model=${encodeURIComponent(model)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': document.querySelector('#api-key').value,
      },
      body: JSON.stringify(payload),
    });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      const detail = typeof body.detail === 'string' ? body.detail : `Request failed (${response.status}). Check the API key and submitted values.`;
      throw new Error(detail);
    }
    const prediction = Number(body.result);
    resultValue.textContent = body.result;
    if (prediction === 1) {
      resultTitle.textContent = 'Will be placed';
      resultCopy.textContent = 'The model predicts this student will be placed.';
    } else if (prediction === 0) {
      resultTitle.textContent = 'Will not be placed';
      resultCopy.textContent = 'The model predicts this student will not be placed.';
      resultCard.classList.add('is-not-placed');
    } else {
      resultTitle.textContent = `Model output: ${body.result}`;
      resultCopy.textContent = 'The model returned an unrecognized placement result.';
    }
    resultCard.classList.add('has-result');
  } catch (error) {
    resultCard.classList.add('is-error');
    resultValue.textContent = '!';
    resultTitle.textContent = 'Forecast unavailable';
    resultCopy.textContent = error instanceof TypeError ? 'Could not reach the API. Confirm the server is running and try again.' : error.message;
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector('span:first-child').textContent = 'Generate forecast';
  }
});

updateProgress();