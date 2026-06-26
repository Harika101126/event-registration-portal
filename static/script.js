// ==========================
// COUNTDOWN TIMER
// ==========================

const eventDate = new Date("July 26, 2026 10:00:00").getTime();

setInterval(() => {

    const now = new Date().getTime();
    const distance = eventDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));

    const hours = Math.floor(
        (distance % (1000 * 60 * 60 * 24))
        / (1000 * 60 * 60)
    );

    const minutes = Math.floor(
        (distance % (1000 * 60 * 60))
        / (1000 * 60)
    );

    const seconds = Math.floor(
        (distance % (1000 * 60))
        / 1000
    );

    const timer = document.getElementById("timer");

    if (timer) {
        timer.innerHTML =
            `${days} Days ${hours} Hours ${minutes} Minutes ${seconds} Seconds`;
    }

}, 1000);