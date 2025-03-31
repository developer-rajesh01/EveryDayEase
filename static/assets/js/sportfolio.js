// Mock data
const services = [
  { id: 1, name: "Haircut", description: "Standard haircut service", price: 30 },
  { id: 2, name: "Massage", description: "60-minute full body massage", price: 60 },
  { id: 3, name: "Nail Care", description: "Manicure and pedicure", price: 40 },
]

const bookings = [
  { id: 1, service: "Haircut", client: "Alice Johnson", date: "2023-06-15", status: "Confirmed" },
  { id: 2, service: "Massage", client: "Bob Smith", date: "2023-06-16", status: "Pending" },
  { id: 3, service: "Nail Care", client: "Carol Davis", date: "2023-06-17", status: "Completed" },
]

// Navigation
document.querySelectorAll(".sidebar a").forEach((link) => {
  link.addEventListener("click", (e) => {
    e.preventDefault()
    const page = e.target.dataset.page
    loadPage(page)
  })
})
var fullname;
var email;
var mobile;
var bio;
function dataTake(name,em) {
  fullname=name
  email=em
  console.log(fullname,email)
  // mobile=mob
  // bio=bi
}

function loadPage(page) {
  const content = document.getElementById("content")
  switch (page) {
    case "dashboard":
      content.innerHTML = generateDashboardHTML()
      renderChart()
      break
    case "profile":
     
     content.innerHTML = generateProfileHTML()
      break
    case "services":
      content.innerHTML = generateServicesHTML()
      break
    case "bookings":
      content.innerHTML = generateBookingsHTML()
      break
  }
}

// Dashboard
function generateDashboardHTML() {
  return `
        <h1>Dashboard</h1>
        <div class="grid">
            <div class="card">
                <h3>Total Earnings</h3>
                <p>$1,234.56</p>
            </div>
            <div class="card">
                <h3>Active Bookings</h3>
                <p>12</p>
            </div>
            <div class="card">
                <h3>Pending Requests</h3>
                <p>3</p>
            </div>
            <div class="card">
                <h3>Average Rating</h3>
                <p>4.8</p>
            </div>
        </div>
        <div class="card">
            <h3>Earnings Overview</h3>
            <canvas id="earningsChart"></canvas>
        </div>
        <div class="card">
            <h3>Recent Bookings</h3>
            <table>
                <thead>
                    <tr>
                        <th>Service</th>
                        <th>Client</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    ${bookings
                      .map(
                        (booking) => `
                        <tr>
                            <td>${booking.service}</td>
                            <td>${booking.client}</td>
                            <td>${booking.date}</td>
                        </tr>
                    `,
                      )
                      .join("")}
                </tbody>
            </table>
        </div>
    `
}

function renderChart() {
  const ctx = document.getElementById("earningsChart").getContext("2d")
  // Import Chart.js library.  This needs to be included in your HTML file as a script tag.  Example: <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [
        {
          label: "Earnings",
          data: [4000, 3000, 5000, 4500, 6000, 5500],
          backgroundColor: "rgba(75, 192, 192, 0.6)",
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  })
}


document.addEventListener("DOMContentLoaded", function () {
  // Get the profile data from HTML
  const profileData = document.getElementById("profile-data");

  // Extract data from `data-*` attributes
  const username = profileData.dataset.username;
  const email = profileData.dataset.email;
  const bio = profileData.dataset.bio;

  console.log("Username:", username);
  console.log("Email:", email);
  console.log("Bio:", bio);

  // Update HTML dynamically
  document.getElementById("name").value = username;
  document.getElementById("email").value = email;
  document.getElementById("bio").textContent = bio;
});

// Profile
function generateProfileHTML() {
  var userProfile = {
    username: "{{ request.user.get_full_name|escapejs }}",
    email: "{{ request.user.email }}",
    phone: "123-456-7890",  // Replace this with actual phone data if available
    bio: "Experienced service provider with 5 years in the industry."  // Replace with actual bio data
};
  return    `
        <h1>Profile Management</h1>
        <form id="profileForm">
            <label for="username">Name:</label>
            <input type="text" id="name" name="name" value="${userProfile.username}" required>
            
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" value="john@example.com" required>
            
            <label for="phone">Phone:</label>
            <input type="tel" id="phone" name="phone" value="123-456-7890" required>
            
            <label for="bio">Bio:</label>
            <textarea id="bio" name="bio" required>Experienced service provider with 5 years in the industry.</textarea>
            
            <button type="submit">Update Profile</button>
        </form>
    `
}

// Services
function generateServicesHTML() {
  return `
        <h1>Services Management</h1>
        <div class="grid">
            ${services
              .map(
                (service) => `
                <div class="card">
                    <h3>${service.name}</h3>
                    <p>${service.description}</p>
                    <p><strong>Price: $${service.price}</strong></p>
                </div>
            `,
              )
              .join("")}
        </div>
        <div class="card">
            <h3>Add New Service</h3>
            <form id="newServiceForm">
                <input type="text" name="name" placeholder="Service Name" required>
                <textarea name="description" placeholder="Description" required></textarea>
                <input type="number" name="price" placeholder="Price" required>
                <button type="submit">Add Service</button>
            </form>
        </div>
    `
}

// Bookings
function generateBookingsHTML() {
  return `
        <h1>Bookings Management</h1>
        <div class="grid">
            ${bookings
              .map(
                (booking) => `
                <div class="card">
                    <h3>${booking.service}</h3>
                    <p><strong>Client:</strong> ${booking.client}</p>
                    <p><strong>Date:</strong> ${booking.date}</p>
                    <select class="booking-status" data-id="${booking.id}">
                        <option value="Pending" ${booking.status === "Pending" ? "selected" : ""}>Pending</option>
                        <option value="Confirmed" ${booking.status === "Confirmed" ? "selected" : ""}>Confirmed</option>
                        <option value="Completed" ${booking.status === "Completed" ? "selected" : ""}>Completed</option>
                        <option value="Cancelled" ${booking.status === "Cancelled" ? "selected" : ""}>Cancelled</option>
                    </select>
                </div>
            `,
              )
              .join("")}
        </div>
    `
}

// Event listeners
document.addEventListener("submit", (e) => {
  if (e.target.id === "profileForm") {
    e.preventDefault()
    // Handle profile update
    alert("Profile updated successfully!")
  } else if (e.target.id === "newServiceForm") {
    e.preventDefault()
    const formData = new FormData(e.target)
    const newService = {
      id: services.length + 1,
      name: formData.get("name"),
      description: formData.get("description"),
      price: Number(formData.get("price")),
    }
    services.push(newService)
    loadPage("services")
  }
})

document.addEventListener("change", (e) => {
  if (e.target.classList.contains("booking-status")) {
    const bookingId = Number(e.target.dataset.id)
    const newStatus = e.target.value
    const bookingIndex = bookings.findIndex((b) => b.id === bookingId)
    if (bookingIndex !== -1) {
      bookings[bookingIndex].status = newStatus
    }
  }
})

// Initial load
loadPage("dashboard")

