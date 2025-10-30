document.addEventListener("DOMContentLoaded", () => {
  const facultySelect = document.getElementById("faculty");
  const departmentSelect = document.getElementById("department");
  const courseSelect = document.getElementById("course");

  // HTMLのdata属性からURLを取得
  const departmentsUrl = facultySelect.dataset.departmentsUrl;
  const coursesUrl = departmentSelect.dataset.coursesUrl;

  // === 学部選択時 ===
  facultySelect.addEventListener("change", async (e) => {
    const facultyId = e.target.value;
    departmentSelect.innerHTML = '<option value="">---------</option>';
    courseSelect.innerHTML = '<option value="">---------</option>';

    if (!facultyId) return;

    try {
      const res = await fetch(`${departmentsUrl}?faculty_id=${facultyId}`);
      if (!res.ok) throw new Error("学科データの取得に失敗しました");
      const data = await res.json();

      data.forEach(dep => {
        const opt = document.createElement("option");
        opt.value = dep.id;
        opt.textContent = dep.name;
        departmentSelect.appendChild(opt);
      });
    } catch (err) {
      console.error(err);
    }
  });

  // === 学科選択時 ===
  departmentSelect.addEventListener("change", async (e) => {
    const departmentId = e.target.value;
    courseSelect.innerHTML = '<option value="">---------</option>';

    if (!departmentId) return;

    try {
      const res = await fetch(`${coursesUrl}?department_id=${departmentId}`);
      if (!res.ok) throw new Error("コースデータの取得に失敗しました");
      const data = await res.json();

      data.forEach(course => {
        const opt = document.createElement("option");
        opt.value = course.id;
        opt.textContent = course.name;
        courseSelect.appendChild(opt);
      });
    } catch (err) {
      console.error(err);
    }
  });
});
