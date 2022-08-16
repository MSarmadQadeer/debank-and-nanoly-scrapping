const textField = document.querySelector('input[type="text"]');
const button = document.querySelector('button');

button.addEventListener('click', function() {
  const text = textField.value;
  console.log(text);
  window.location = `/${text}`;
} );