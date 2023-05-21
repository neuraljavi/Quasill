// FUNCIÓN CREADA POR ALEJANDRA

//EL TEXTO SE ESCRIBE SOLO EN INPUTDEMO
const text = "My wrist hurts and I have headaches all day. I can't sleep.";
const typingDemo = document.getElementById("inputDemo");
let i = 0;

function typeWriter() {
  if (i < text.length) {
    typingDemo.innerHTML += text.charAt(i);
    i++;
    setTimeout(typeWriter, 50);
  }
}
typeWriter();