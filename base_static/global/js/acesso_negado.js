let countdown = 10;

function updateCountdown() {
    document.getElementById("timer").textContent = countdown;
    if (countdown === 0) {
        window.location.href = '/';  // redireciona para home (ou perfil, etc.)
    } else {
        countdown--;
        setTimeout(updateCountdown, 1000);
    }
}

window.onload = updateCountdown;