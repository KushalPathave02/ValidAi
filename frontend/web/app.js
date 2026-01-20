(() => {
  const backendUrl = 'http://localhost:8000';

  const form = document.getElementById('validator-form');
  const nameEl = document.getElementById('name');
  const emailEl = document.getElementById('email');
  const ageEl = document.getElementById('age');
  const countryEl = document.getElementById('country');
  const phoneEl = document.getElementById('phone');

  const resultSection = document.getElementById('result');
  const statusBadge = document.getElementById('status-badge');
  const errorsBlock = document.getElementById('errors-block');
  const warningsBlock = document.getElementById('warnings-block');
  const errorsList = document.getElementById('errors-list');
  const warningsList = document.getElementById('warnings-list');
  const toast = document.getElementById('toast');
  const invalidNameBlock = document.getElementById('invalid-name-block');
  const invalidNameValue = document.getElementById('invalid-name-value');

  const fillValidBtn = document.getElementById('fill-valid');
  const fillInvalidBtn = document.getElementById('fill-invalid');
  const submitBtn = document.getElementById('submit');

  function showToast(message) {
    toast.textContent = message;
    toast.classList.remove('hidden');
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
      toast.classList.add('hidden');
    }, 2500);
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Validating…' : 'Validate';
  }

  function toPayload() {
    return {
      name: nameEl.value,
      email: emailEl.value,
      age: ageEl.value,
      country: countryEl.value,
      phone: phoneEl.value,
    };
  }

  function renderResult(data) {
    resultSection.classList.remove('hidden');

    const isValid = data.is_valid === true;
    statusBadge.textContent = isValid ? 'Valid' : 'Invalid';
    statusBadge.classList.remove('success','error');
    statusBadge.classList.add(isValid ? 'success' : 'error');

    const errors = Array.isArray(data.errors) ? data.errors : [];
    const hasNameError = errors.some(e => typeof e === 'string' && e.toLowerCase().startsWith('name'));

    if (!isValid && hasNameError) {
      invalidNameBlock.classList.remove('hidden');
      invalidNameValue.textContent = nameEl.value.trim() || '(empty)';
    } else {
      invalidNameBlock.classList.add('hidden');
      invalidNameValue.textContent = '';
    }

    // Errors
    errorsList.innerHTML = '';
    if (errors.length) {
      errorsBlock.classList.remove('hidden');
      errors.forEach(e => {
        const li = document.createElement('li');
        li.textContent = e;
        errorsList.appendChild(li);
      });
    } else {
      errorsBlock.classList.add('hidden');
    }

    // Warnings
    warningsList.innerHTML = '';
    const warnings = Array.isArray(data.warnings) ? data.warnings : [];
    if (warnings.length) {
      warningsBlock.classList.remove('hidden');
      warnings.forEach(w => {
        const li = document.createElement('li');
        li.textContent = w;
        warningsList.appendChild(li);
      });
    } else {
      warningsBlock.classList.add('hidden');
    }
  }

  async function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = toPayload();
      const res = await fetch(`${backendUrl}/validate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        showToast('Validation failed. Please try again.');
        return;
      }
      const data = await res.json();
      renderResult(data);
    } catch (err) {
      console.error(err);
      showToast('Network error. Is the API running on :8000?');
    } finally {
      setLoading(false);
    }
  }

  function fillValid() {
    nameEl.value = 'Aarav Sharma';
    emailEl.value = 'aarav.sharma@example.com';
    ageEl.value = '28';
    countryEl.value = 'IN';
    phoneEl.value = '+919876543210';
  }

  function fillInvalid() {
    nameEl.value = '';
    emailEl.value = 'not-an-email';
    ageEl.value = '-1';
    countryEl.value = 'XX';
    phoneEl.value = '12345';
  }

  form.addEventListener('submit', onSubmit);
  fillValidBtn.addEventListener('click', fillValid);
  fillInvalidBtn.addEventListener('click', fillInvalid);
})();

