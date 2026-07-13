const CONTACT = {
  facebook: "https://www.facebook.com/profile.php?id=61569858206413",
  messenger: "https://m.me/rld.resorts.siq",
  whatsappNumber: "+639977448260",
  emailAddress: "rldresort775@gmail.com",
  maps: "https://maps.app.goo.gl/e8auYz2ATanAsXaa8",
};
const FORM_ENDPOINT = `https://formsubmit.co/ajax/${CONTACT.emailAddress}`;

const header = document.querySelector("#site-header");
const navToggle = document.querySelector(".nav-toggle");
const navigation = document.querySelector("#primary-navigation");
const form = document.querySelector("#reservation-form");
const submitButton = form.querySelector(".submit-button");
const submitLabel = form.querySelector(".submit-label");
const channelInputs = [...form.querySelectorAll('input[name="channel"]')];
const toast = document.querySelector("#toast");
const dateInput = form.querySelector('input[name="date"]');
const gallery = document.querySelector("#resort-gallery");
const lightbox = document.querySelector("#gallery-lightbox");
const lightboxImage = document.querySelector("#lightbox-image");
const lightboxCaption = document.querySelector("#lightbox-caption");
const lightboxCount = document.querySelector("#lightbox-count");
const lightboxThumbnails = document.querySelector("#lightbox-thumbnails");
const lightboxClose = document.querySelector(".lightbox-close");
const lightboxPrev = document.querySelector(".lightbox-prev");
const lightboxNext = document.querySelector(".lightbox-next");
const openFullGallery = document.querySelector("#open-full-gallery");
const galleryButtons = [...gallery.querySelectorAll(".gallery-open")];
const galleryItems = galleryButtons.map((button) => {
  const image = button.querySelector("img");
  return {
    src: button.dataset.full,
    alt: image.alt,
    caption: button.dataset.caption || image.alt,
  };
});
let toastTimer;
let activeGalleryIndex = 0;

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

function updateSubmitLabel() {
  const channel = form.querySelector('input[name="channel"]:checked').value;
  const labels = {
    messenger: "Continue to Messenger",
    whatsapp: "Continue to WhatsApp",
    email: "Send inquiry by email",
  };
  submitLabel.textContent = labels[channel];
}

async function sendEmailInquiry(data, message) {
  const response = await fetch(FORM_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({
      name: data.get("name"),
      email: data.get("email"),
      phone: data.get("phone") || "Not provided",
      preferred_date: data.get("date"),
      visit_type: data.get("visit"),
      number_of_guests: data.get("guests"),
      notes: data.get("notes") || "None",
      message,
      _replyto: data.get("email"),
      _subject: `New RLD Resort reservation inquiry from ${data.get("name")}`,
      _template: "table",
      _honey: data.get("_honey") || "",
    }),
  });

  const result = await response.json().catch(() => ({}));
  if (!response.ok || result.success === false || result.success === "false") {
    throw new Error(result.message || "Unable to send inquiry");
  }
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
  if (!lightbox.open) return;
  if (event.key === "ArrowLeft") showGalleryPhoto(activeGalleryIndex - 1);
  if (event.key === "ArrowRight") showGalleryPhoto(activeGalleryIndex + 1);
});

window.addEventListener("scroll", updateHeader, { passive: true });
updateHeader();
channelInputs.forEach((input) => input.addEventListener("change", updateSubmitLabel));
updateSubmitLabel();

function showGalleryPhoto(index) {
  activeGalleryIndex = (index + galleryItems.length) % galleryItems.length;
  const item = galleryItems[activeGalleryIndex];

  lightboxImage.src = item.src;
  lightboxImage.alt = item.alt;
  lightboxCaption.textContent = item.caption;
  lightboxCount.textContent = `${activeGalleryIndex + 1} / ${galleryItems.length}`;

  const thumbnails = [...lightboxThumbnails.querySelectorAll(".lightbox-thumbnail")];
  thumbnails.forEach((thumbnail, thumbnailIndex) => {
    const isActive = thumbnailIndex === activeGalleryIndex;
    thumbnail.classList.toggle("active", isActive);
    thumbnail.setAttribute("aria-current", isActive ? "true" : "false");
  });

  const activeThumbnail = thumbnails[activeGalleryIndex];
  if (activeThumbnail) {
    lightboxThumbnails.scrollTo({
      left: activeThumbnail.offsetLeft - lightboxThumbnails.clientWidth / 2 + activeThumbnail.offsetWidth / 2,
      behavior: "smooth",
    });
  }
}

function openGallery(index = 0) {
  if (typeof lightbox.showModal !== "function") {
    window.open(galleryItems[index].src, "_blank", "noopener");
    return;
  }

  lightbox.showModal();
  showGalleryPhoto(index);
}

galleryItems.forEach((item, index) => {
  const button = document.createElement("button");
  const image = document.createElement("img");
  button.className = "lightbox-thumbnail";
  button.type = "button";
  button.setAttribute("aria-label", `View photo ${index + 1}: ${item.caption}`);
  image.src = item.src;
  image.alt = "";
  image.loading = "lazy";
  button.appendChild(image);
  button.addEventListener("click", () => showGalleryPhoto(index));
  lightboxThumbnails.appendChild(button);
});

gallery.addEventListener("click", (event) => {
  const button = event.target.closest(".gallery-open");
  if (!button) return;
  openGallery(galleryButtons.indexOf(button));
});

openFullGallery.addEventListener("click", () => openGallery(0));
lightboxPrev.addEventListener("click", () => showGalleryPhoto(activeGalleryIndex - 1));
lightboxNext.addEventListener("click", () => showGalleryPhoto(activeGalleryIndex + 1));
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
    `Email: ${data.get("email")}`,
    `Mobile number: ${data.get("phone") || "Not provided"}`,
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

  if (channel === "email") {
    submitButton.disabled = true;
    submitLabel.textContent = "Sending inquiry...";

    try {
      await sendEmailInquiry(data, message);
      form.reset();
      updateSubmitLabel();
      showToast("Reservation inquiry sent directly to RLD Resort.");
    } catch {
      const whatsappInput = form.querySelector('input[value="whatsapp"]');
      whatsappInput.checked = true;
      updateSubmitLabel();
      showToast("Email delivery is unavailable right now. Your details are preserved; continue through WhatsApp instead.");
    } finally {
      submitButton.disabled = false;
    }
    return;
  }

  const copied = await copyInquiry(message);
  const notice = copied
    ? "Your inquiry is copied. Paste it into Messenger, then press Send."
    : "Opening Messenger so you can review and send your inquiry.";

  showToast(notice);
  window.setTimeout(() => window.open(CONTACT.messenger, "_blank", "noopener"), 350);
});
