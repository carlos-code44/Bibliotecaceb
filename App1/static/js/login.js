// const switchers = [...document.querySelectorAll('.switcher')]

// switchers.forEach(item => {
// 	item.addEventListener('click', function() {
// 		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
// 		this.parentElement.classList.add('is-active')
// 	})
// })



// codigo js del segundo login

const registerButton = document.getElementById("register");
const loginButton = document.getElementById("login");
const container = document.getElementById("container");

registerButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});

loginButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});


function showToast(message, type = 'info') {
	const toastContainer = document.getElementById('toast-container');
	const toast = document.createElement('div');
	toast.className = `toast ${type}`;
	toast.textContent = message;
	
	toastContainer.appendChild(toast);
	
	setTimeout(() => {
	  toast.classList.add('show');
	}, 100);
  
	setTimeout(() => {
	  toast.classList.remove('show');
	  setTimeout(() => {
		toastContainer.removeChild(toast);
	  }, 300);
	}, 3000);
  }