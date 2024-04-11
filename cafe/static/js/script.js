window.onload = function () {
  // Check if there's a scroll position stored in sessionStorage
  if (sessionStorage.getItem('scrollPosition')) {
    // If there is, scroll to that position
    window.scroll({
      top: sessionStorage.getItem('scrollPosition'),
      behavior: 'auto'
    });
    // Then, remove the stored scroll position
    sessionStorage.removeItem('scrollPosition');
  }
};

window.onbeforeunload = function () {
  // Before the page is unloaded (refreshed), store the current scroll position
  sessionStorage.setItem('scrollPosition', window.scrollY);
};

var logID = 'log',
  log = $('<div id="' + logID + '"></div>');
$('body').append(log);
$('[type*="radio"]').change(function () {
  var me = $(this);
  log.html(me.attr('value'));
});

// To show all products based on the selected category button
function filterProducts(category) {
  // If no category is selected, show all product containers
  if (category === null) {
    document.querySelectorAll('.products-container').forEach(function (container) {
      container.style.display = 'block';
    });
  } else {
    // Hide all product containers
    document.querySelectorAll('.products-container').forEach(function (container) {
      container.style.display = 'none';
    });

    // Show products of the selected category
    document.querySelectorAll(`.products-container[data-category="${category}"]`).forEach(function (container) {
      container.style.display = 'block';
    });
  }
}

// To show all products' headings based on the selected category button
function filterHeadings(category) {
  // If no category is selected, show all headings
  if (category === null) {
    document.querySelectorAll('.category-heading').forEach(function (heading) {
      heading.style.display = 'block';
    });
  } else {
    // Show headings of the selected category and hide others
    document.querySelectorAll('.category-heading').forEach(function (heading) {
      if (heading.dataset.category === category) {
        heading.style.display = 'block';
      } else {
        heading.style.display = 'none';
      }
    });
  }
}

function toggleFilter(category) {
  // Get the clicked button
  var button = document.querySelector(`.category-button[data-category="${category}"]`);

  // Check if the clicked button is already active
  var isActive = button.classList.contains('active');

  // Remove the active class from all buttons
  document.querySelectorAll('.category-button').forEach(function (btn) {
    btn.classList.remove('active', 'selected');
  });

  // If the clicked button was NOT active, apply the active and selected classes
  if (!isActive) {
    button.classList.add('active', 'selected');

    // Apply filters for the selected category
    filterProducts(category);
    filterHeadings(category);
  } else {
    // Reset filters if the clicked button was already active
    filterProducts(null);
    filterHeadings(null);
  }
}

// Check if the modal state exists in sessionStorage
var modalState = sessionStorage.getItem('modalState');

// If the modalState is 'open', show the modal
if (modalState === 'open') {
  var myOffcanvas = new bootstrap.Offcanvas(document.getElementById('cartOffcanvas'));
  myOffcanvas.show();
}

// When the modal is shown, update the modal state to 'open' in sessionStorage
document.getElementById('cartOffcanvas').addEventListener('shown.bs.offcanvas', function () {
  sessionStorage.setItem('modalState', 'open');
});

// When the modal is hidden, update the modal state to 'closed' in sessionStorage
document.getElementById('cartOffcanvas').addEventListener('hidden.bs.offcanvas', function () {
  sessionStorage.setItem('modalState', 'closed');
});
