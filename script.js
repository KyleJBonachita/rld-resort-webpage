const CONTACT = {
  facebook: "https://www.facebook.com/profile.php?id=61569858206413",
  messenger: "https://m.me/rld.resorts.siq",
  whatsappNumber: "+639977448260",
  emailAddress: "rldresort775@gmail.com",
  maps: "https://maps.app.goo.gl/e8auYz2ATanAsXaa8",
};

const header = document.querySelector("#site-header");
const navToggle = document.querySelector(".nav-toggle");
const navigation = document.querySelector("#primary-navigation");
const form = document.querySelector("#reservation-form");
const toast = document.querySelector("#toast");
const dateInput = form.querySelector('input[name="date"]');
const gallery = document.querySelector("#resort-gallery");
const lightbox = document.querySelector("#gallery-lightbox");
const lightboxImage = document.querySelector("#lightbox-image");
const lightboxCaption = document.querySelector("#lightbox-caption");
const lightboxClose = document.querySelector(".lightbox-close");
let toastTimer;

document.querySelector("#current-year").textContent = new Date().getFullYear();
dateInput.min = new Date().toISOString().split("T")[0];

function updateHeader() {
  header.classList.toggle("scrolled", window.scrollY > 24);
}

function closeMenu() {
  navigation.classList.remove("open");
  header.classList.remove("menu-visible");
  navToggle.setAttribute("aria-expanded", "false");
  navToggle.setAttribute("aria-label", "Open menu");
  document.body.classList.remove("menu-open");
}

function showToast(message) {
  window.clearTimeout(toastTimer);
  toast.textContent = message;
  toast.classList.add("visible");
  toastTimer = window.setTimeout(() => toast.classList.remove("visible"), 4200);
}

async function copyInquiry(message) {
  try {
    await navigator.clipboard.writeText(message);
    return true;
  } catch {
    const textArea = document.createElement("textarea");
    textArea.value = message;
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    document.body.appendChild(textArea);
    textArea.select();
    const copied = document.execCommand("copy");
    textArea.remove();
    return copied;
  }
}

navToggle.addEventListener("click", () => {
  const isOpen = navigation.classList.toggle("open");
  header.classList.toggle("menu-visible", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));
  navToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
  document.body.classList.toggle("menu-open", isOpen);
});

navigation.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeMenu();
});

window.addEventListener("scroll", updateHeader, { passive: true });
updateHeader();

gallery.addEventListener("click", (event) => {
  const button = event.target.closest(".gallery-open");
  if (!button) return;

  const previewImage = button.querySelector("img");
  const fullImage = button.dataset.full;
  const caption = button.dataset.caption || previewImage.alt;

  if (typeof lightbox.showModal !== "function") {
    window.open(fullImage, "_blank", "noopener");
    return;
  }

  lightboxImage.src = fullImage;
  lightboxImage.alt = previewImage.alt;
  lightboxCaption.textContent = caption;
  lightbox.showModal();
});

lightboxClose.addEventListener("click", () => lightbox.close());

lightbox.addEventListener("click", (event) => {
  const bounds = lightbox.getBoundingClientRect();
  const clickedOutside =
    event.clientX < bounds.left ||
    event.clientX > bounds.right ||
    event.clientY < bounds.top ||
    event.clientY > bounds.bottom;

  if (clickedOutside) lightbox.close();
});

lightbox.addEventListener("close", () => {
  lightboxImage.removeAttribute("src");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const message = [
    "Hello RLD Resort! I would like to request a reservation.",
    "",
    `Name: ${data.get("name")}`,
    `Preferred date: ${data.get("date")}`,
    `Type of visit: ${data.get("visit")}`,
    `Number of guests: ${data.get("guests")}`,
    `Notes: ${data.get("notes") || "None"}`,
    "",
    "Please let me know the availability, rates, and booking requirements. Thank you!",
  ].join("\n");

  const channel = data.get("channel");

  if (channel === "whatsapp" && CONTACT.whatsappNumber) {
    const number = CONTACT.whatsappNumber.replace(/\D/g, "");
    window.open(`https://wa.me/${number}?text=${encodeURIComponent(message)}`, "_blank", "noopener");
    return;
  }

  if (channel === "email" && CONTACT.emailAddress) {
    window.location.href = `mailto:${CONTACT.emailAddress}?subject=${encodeURIComponent("Reservation inquiry for RLD Resort")}&body=${encodeURIComponent(message)}`;
    return;
  }

  const copied = await copyInquiry(message);
  const missingChannel = channel === "whatsapp" || channel === "email";
  const notice = missingChannel
    ? `${channel === "whatsapp" ? "WhatsApp" : "Email"} details have not been added yet. Opening Messenger instead${copied ? "; your inquiry is copied and ready to paste." : "."}`
    : copied
      ? "Your inquiry is copied. Paste it into Messenger to send."
      : "Opening Messenger so you can send your inquiry.";

  showToast(notice);
  window.setTimeout(() => window.open(CONTACT.messenger, "_blank", "noopener"), 350);
});
