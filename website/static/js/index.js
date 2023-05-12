
//EL TEXTO SE ESCRIBE SOLO EN INPUTDEMO
const text = "Me duele la muñeca izquierda y vomito sangre todas las noches :(";
const typingDemo = document.getElementById("inputDemo");
let i = 0;
setInterval(() => {
  if (i <= text.length) {
    typingDemo.innerHTML = text.slice(0, i);
    i++;
  }
}, 50);
const btnDemo = document.getElementById("btnDemo");
const containerRight = document.querySelector(".container-right");
const originalContent = containerRight.innerHTML; // Store original content

//BTNDEMO CAMBIA EL CONTENIDO DE CONTAINER-RIGHT

btnDemo.addEventListener("click", () => {
  // Change the content of containerRight
  containerRight.innerHTML = `
    <div class="demo">
    <h2>DIAGNÓSTICO: COVID-19</h2>
    <h2>PROBABILIDAD: 150%</h2>
    <div class="circle"></div>
    </div>
    <div class="demo">
    <h2>DIAGNÓSTICO: ANEMIA</h2>
    <h2>PROBABILIDAD: 99%</h2>
    <div class="circle"></div>
    </div>
`;
  setTimeout(() => {
    containerRight.innerHTML = originalContent;
  }, 7000);
});

// CREAR CUENTA - VIEW: SIGNUP
function submitForm() {
    document.getElementById("signupForm").submit();
}
function updateUser() {
    console.log("updateUser function called");
    document.getElementById("edit-delete").submit();
    console.log("form submitted");
}

function deleteUser() {
    console.log("deleteUser function called");
    document.getElementById("edit-delete").submit();
    console.log("form submitted");
}

