document.addEventListener("DOMContentLoaded", () => {
    loadPatients();

    // Dark mode
    const saved = localStorage.getItem("theme");
    if (saved === "dark") document.body.classList.add("dark");

    themeToggle.onclick = () => {
        document.body.classList.toggle("dark");
        localStorage.setItem(
            "theme",
            document.body.classList.contains("dark") ? "dark" : "light"
        );
    };
});

/* ---------- HELPERS ---------- */
function val(id) {
    return document.getElementById(id).value.trim();
}

function num(id) {
    const v = Number(document.getElementById(id).value);
    return Number.isNaN(v) ? null : v;
}

/* ---------- LOAD ---------- */
function loadPatients() {
    fetch("/view")
        .then(r => r.json())
        .then(data => {
            table.innerHTML = "";
            Object.entries(data).forEach(([id, p]) => {
                const tr = document.createElement("tr");

                tr.innerHTML = `
                    <td>${id}</td>
                    <td>${p.name}</td>
                    <td>${p.city}</td>
                    <td>${p.bmi}</td>
                    <td><span class="status ${p.verdict}">${p.verdict}</span></td>
                    <td>
                        <button class="btn ghost"
                            onclick="event.stopPropagation(); deletePatient('${id}')">
                            Delete
                        </button>
                    </td>
                `;

                tr.onclick = () => fillForm(id, p);
                table.appendChild(tr);
            });
        });
}

/* ---------- FORM AUTO-FILL ---------- */
function fillForm(id, p) {
    pid.value = id;
    name.value = p.name;
    city.value = p.city;
    age.value = p.age;
    gender.value = p.gender;
    height.value = p.height;
    weight.value = p.weight;
}

/* ---------- ADD ---------- */
function addPatient() {
    const payload = {
        id: val("pid"),
        name: val("name"),
        city: val("city"),
        age: num("age"),
        gender: val("gender"),
        height: num("height"),
        weight: num("weight")
    };

    for (const [k, v] of Object.entries(payload)) {
        if (v === "" || v === null) {
            alert(`Invalid or missing field: ${k}`);
            return;
        }
    }

    fetch("/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(r => {
        if (!r.ok) throw new Error("Add failed");
        return r.json();
    })
    .then(loadPatients)
    .catch(e => alert(e.message));
}

/* ---------- UPDATE ---------- */
function updatePatient() {
    const id = val("pid");
    if (!id) {
        alert("Patient ID required for update");
        return;
    }

    const updates = {};
    if (val("name")) updates.name = val("name");
    if (val("city")) updates.city = val("city");
    if (val("gender")) updates.gender = val("gender");
    if (num("age") !== null) updates.age = num("age");
    if (num("height") !== null) updates.height = num("height");
    if (num("weight") !== null) updates.weight = num("weight");

    if (Object.keys(updates).length === 0) {
        alert("Nothing to update");
        return;
    }

    fetch(`/edit/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates)
    })
    .then(r => {
        if (!r.ok) throw new Error("Update failed");
        return r.json();
    })
    .then(loadPatients)
    .catch(e => alert(e.message));
}

/* ---------- DELETE ---------- */
function deletePatient(id) {
    fetch(`/delete/${id}`, { method: "DELETE" })
        .then(loadPatients);
}
