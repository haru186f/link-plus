document.addEventListener("DOMContentLoaded", function() {
  const collegeSelect = document.getElementById("id_college");
  const departmentSelect = document.getElementById("id_department");
  const courseSelect = document.getElementById("id_course");
  const gradeSelect = document.getElementById("id_grade");
  const classSelect = document.getElementById("id_class_number");
  const busSelect = document.getElementById("id_bus");

  // 🔹「値が空の場合のみ」初期化
  if (!departmentSelect.value) {
    departmentSelect.innerHTML = '<option value="">---------</option>';
  }
  if (!courseSelect.value) {
    courseSelect.innerHTML = '<option value="">---------</option>';
  }
  if (!gradeSelect.value) {
    gradeSelect.innerHTML = '<option value="">---------</option>';
  }
  if (!classSelect.value) {
    classSelect.innerHTML = '<option value="">---------</option>';
  }
  if (!busSelect.value) {
    busSelect.innerHTML = '<option value="">---------</option>';
  }

  // 学部変更 → 学科更新
  collegeSelect.addEventListener("change", function() {
    const collegeId = this.value;
    const url = this.dataset.departmentsUrl;

    departmentSelect.innerHTML = '<option value="">---------</option>';
    courseSelect.innerHTML = '<option value="">---------</option>';
    gradeSelect.innerHTML = '<option value="">---------</option>';
    classSelect.innerHTML = '<option value="">---------</option>';

    if (collegeId) {
      fetch(`${url}?college_id=${collegeId}`)
        .then(response => response.json())
        .then(data => {
          data.forEach(dept => {
            const option = document.createElement("option");
            option.value = dept.id;
            option.textContent = dept.name;
            departmentSelect.appendChild(option);
          });
        })
        .catch(err => console.error("学科取得エラー:", err));
    }
  });

  // 学科変更 → コース・学年更新
  departmentSelect.addEventListener("change", function() {
    const departmentId = this.value;
    const coursesUrl = this.dataset.coursesUrl;
    const gradesUrl = this.dataset.gradesUrl;

    courseSelect.innerHTML = '<option value="">---------</option>';
    gradeSelect.innerHTML = '<option value="">---------</option>';
    classSelect.innerHTML = '<option value="">---------</option>';

    if (departmentId) {
      // コース取得
      fetch(`${coursesUrl}?department_id=${departmentId}`)
        .then(response => response.json())
        .then(data => {
          data.forEach(course => {
            const option = document.createElement("option");
            option.value = course.id;
            option.textContent = course.name;
            courseSelect.appendChild(option);
          });
        })
        .catch(err => console.error("コース取得エラー:", err));

      // 学年取得
      fetch(`${gradesUrl}?department_id=${departmentId}`)
        .then(response => response.json())
        .then(data => {
          for (let i = 1; i <= data.max_grade; i++) {
            const option = document.createElement("option");
            option.value = i;
            option.textContent = `${i}年`;
            gradeSelect.appendChild(option);
          }
        })
        .catch(err => console.error("学年取得エラー:", err));
    }
  });

  // 学年変更 → クラス更新
  gradeSelect.addEventListener("change", function() {
    const gradeValue = this.value;

    classSelect.innerHTML = '<option value="">---------</option>';

    if (gradeValue) {
      for (let i = 1; i <= 4; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = `${i}組`;
        classSelect.appendChild(option);
      }
    }
  });
});
