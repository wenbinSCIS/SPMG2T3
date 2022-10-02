// using the extension es6-string-html by Tobermory (so /*html*/`` has html highlighting)

// getting the user-category (manager/staff/hr) from sessionStorage
const user_category = window.sessionStorage.getItem("user-category");

// navbar as template-literal-string (i.e. using ${}, can work as if it was a python f-string (e.g. F"{var}"))
export default /*html*/`
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <div class="col-2"></div>
      <a class="navbar-brand" href="home.html">Learning Journey Planner</a>
      <button class="navbar-toggler" type="text" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="home.html">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="availableroles.html">Roles</a>
          </li>
          <li class="nav-item">
            <form class="d-inline-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
          </li>
        </ul>
        ${user_category
          // if user category not null, dropdown with welcome/category
          ? /*html*/`
          <div class="dropdown">
            <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
              Welcome, ${user_category}
            </button>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton1">
              <li><a class="dropdown-item" href="#">My Learning Journey</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#">Logout</a></li>
            </ul>
          </div>
          `
          // if user category is null
          : /*html*/`
          <div>
            <button class="btn btn-secondary" type="button">
              <!-- currently nothing added yet -->
              Login
            </button>
          </div>
          `
        }
      </div>
      <div class="col-2"></div>
    </div>
  </nav>
`;



/*
<div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
    <!-- ternary-conditional-operator, checking if not null, then welcome, otherwise a fallback -->
    ${user_category ? 'Welcome, ' + user_category : 'Profile'}
  </button>
  <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton1">
    <li><a class="dropdown-item" href="#">My Learning Journey</a></li>
    <li><hr class="dropdown-divider"></li>
    <li><a class="dropdown-item" href="#">Logout</a></li>
  </ul>
</div>
*/

