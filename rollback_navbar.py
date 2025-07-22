import os
import shutil

# Check if base_new.html exists and restore original base.html
if os.path.exists('app/templates/base_new.html'):
    # Backup the current base.html just in case
    shutil.copy('app/templates/base.html', 'app/templates/base_modified.html')
    print("Current base.html backed up to base_modified.html")
    
    # Delete the includes directory if it exists
    if os.path.exists('app/templates/includes'):
        shutil.rmtree('app/templates/includes')
        print("Removed includes directory")
    
    # Delete the navbar.css file if it exists
    if os.path.exists('app/static/css/navbar.css'):
        os.remove('app/static/css/navbar.css')
        print("Removed navbar.css file")
    
    # Create a new base.html without the include
    with open('app/templates/base.html', 'r') as f:
        content = f.read()
    
    # Remove the include line
    content = content.replace("{% include 'includes/navbar.html' %}", """    <nav class="navbar navbar-expand-lg modern-navbar sticky-top">
        <div class="container">
            <a class="navbar-brand animate__animated animate__fadeInLeft" href="{{ url_for('main.index') }}">
                <div class="brand-logo">
                    <i class="fas fa-hands-helping"></i>
                </div>
                JanSamvaad
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto animate__animated animate__fadeInDown">
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == url_for('main.index') %}active{% endif %}" href="{{ url_for('main.index') }}">
                            <i class="fas fa-home"></i> Home
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == url_for('hazards.report_hazard') %}active{% endif %}" href="{{ url_for('hazards.report_hazard') }}">
                            <i class="fas fa-exclamation-triangle"></i> Report Hazard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == url_for('hazards.view_hazards') %}active{% endif %}" href="{{ url_for('hazards.view_hazards') }}">
                            <i class="fas fa-map-marked-alt"></i> View Hazards
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == url_for('corruption.report_corruption') %}active{% endif %}" href="{{ url_for('corruption.report_corruption') }}">
                            <i class="fas fa-gavel"></i> Report Corruption
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.path == url_for('trees_bp.plant_tree') %}active{% endif %}" href="{{ url_for('trees_bp.plant_tree') }}">
                            <i class="fas fa-seedling"></i> Plant a Tree
                        </a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="resourcesDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-book"></i> Resources
                        </a>
                        <div class="dropdown-menu mega-menu p-4">
                            <div class="row">
                                <div class="col-md-4 mb-3 mb-md-0">
                                    <h6 class="mega-menu-title">Government Schemes</h6>
                                    <a href="{{ url_for('schemes.view_schemes') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-landmark"></i> All Schemes
                                    </a>
                                    <a href="{{ url_for('schemes.view_schemes', category='agriculture') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-tractor"></i> Agriculture
                                    </a>
                                    <a href="{{ url_for('schemes.view_schemes', category='education') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-graduation-cap"></i> Education
                                    </a>
                                    <a href="{{ url_for('schemes.view_schemes', category='health') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-heartbeat"></i> Health
                                    </a>
                                </div>
                                <div class="col-md-4 mb-3 mb-md-0">
                                    <h6 class="mega-menu-title">Public Services</h6>
                                    <a href="{{ url_for('services.view_services') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-building"></i> All Services
                                    </a>
                                    <a href="{{ url_for('services.view_services', category='utilities') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-bolt"></i> Utilities
                                    </a>
                                    <a href="{{ url_for('services.view_services', category='transportation') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-bus"></i> Transportation
                                    </a>
                                    <a href="{{ url_for('services.view_services', category='emergency') }}" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-ambulance"></i> Emergency
                                    </a>
                                </div>
                                <div class="col-md-4">
                                    <h6 class="mega-menu-title">Community</h6>
                                    <a href="#" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-users"></i> Community Forums
                                    </a>
                                    <a href="#" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-hands-helping"></i> Volunteer
                                    </a>
                                    <a href="#" class="mega-menu-item text-decoration-none">
                                        <i class="fas fa-book-reader"></i> Education Resources
                                    </a>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
                <ul class="navbar-nav auth-buttons animate__animated animate__fadeInRight">
                    {% if session.get('user_id') %}
                    <li class="nav-item dropdown user-dropdown">
                        <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
                            <div class="user-avatar">
                                <i class="fas fa-user"></i>
                            </div>
                            {{ session.get('username') }}
                            <i class="fas fa-chevron-down ms-2" style="font-size: 0.8rem;"></i>
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><a class="dropdown-item" href="{{ url_for('auth.profile') }}"><i class="fas fa-user me-2 text-primary"></i>My Profile</a></li>
                            <li><a class="dropdown-item" href="{{ url_for('trees_bp.rewards_page') }}"><i class="fas fa-gift me-2 text-primary"></i>My Rewards</a></li>
                            <li><a class="dropdown-item" href="#"><i class="fas fa-bell me-2 text-primary"></i>Notifications</a></li>
                            <li><a class="dropdown-item" href="#"><i class="fas fa-cog me-2 text-primary"></i>Settings</a></li>
                            {% if session.get('is_admin') %}
                            <li><a class="dropdown-item" href="{{ url_for('admin.dashboard') }}"><i class="fas fa-user-shield me-2 text-danger"></i>Admin Dashboard</a></li>
                            {% endif %}
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{{ url_for('auth.logout') }}"><i class="fas fa-sign-out-alt me-2 text-danger"></i>Logout</a></li>
                        </ul>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link login-btn" href="{{ url_for('auth.login') }}">
                            <i class="fas fa-sign-in-alt"></i> Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link register-btn" href="{{ url_for('auth.register') }}">
                            <i class="fas fa-user-plus"></i> Register
                        </a>
                    </li>
                    <li class="nav-item ms-2">
                        <a class="nav-link admin-btn" href="{{ url_for('admin.login') }}">
                            <i class="fas fa-user-shield"></i> Admin
                        </a>
                    </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>""")
    
    # Remove the navbar.css link
    content = content.replace('<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/navbar.css\') }}">', '')
    
    # Write the updated content back to base.html
    with open('app/templates/base.html', 'w') as f:
        f.write(content)
    
    print("Navbar rollback complete!")
else:
    print("No changes to rollback.")