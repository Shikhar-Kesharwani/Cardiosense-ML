// static/3d_heart.js
const init3DHeart = () => {
    const container = document.getElementById('canvas-container');
    if (!container) return;

    // Scene setup
    const scene = new THREE.Scene();
    
    // Camera setup
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 30;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Heart Shape generation using Parametric Equation
    const particles = 3000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particles * 3);
    const colors = new Float32Array(particles * 3);

    const color1 = new THREE.Color(0xff4b4b); // Bright Red
    const color2 = new THREE.Color(0xff0080); // Deep Pink/Purple

    for (let i = 0; i < particles; i++) {
        // Generate random t and u for parametric heart equation
        const t = Math.PI * 2 * Math.random();
        const u = Math.random();
        
        // Heart equation
        const x = 16 * Math.pow(Math.sin(t), 3);
        const y = 13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t);
        const z = (Math.random() - 0.5) * 5; // give it some depth

        // Scale and add randomness
        const scale = 0.5 + (u * 0.5);
        
        positions[i * 3] = x * scale;
        positions[i * 3 + 1] = y * scale;
        positions[i * 3 + 2] = z * scale;

        // Mix colors
        const mixedColor = color1.clone().lerp(color2, Math.random());
        colors[i * 3] = mixedColor.r;
        colors[i * 3 + 1] = mixedColor.g;
        colors[i * 3 + 2] = mixedColor.b;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    // Particle material
    const material = new THREE.PointsMaterial({
        size: 0.15,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });

    const particleSystem = new THREE.Points(geometry, material);
    scene.add(particleSystem);

    // Handle Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Mouse interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;
    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX);
        mouseY = (event.clientY - windowHalfY);
    });

    // Animation Loop
    let time = 0;
    const animate = () => {
        requestAnimationFrame(animate);
        time += 0.05;

        // Heartbeat pulse effect
        const scale = 1 + 0.05 * Math.sin(time) + 0.02 * Math.sin(time * 2);
        particleSystem.scale.set(scale, scale, scale);

        // Subtle rotation
        targetX = mouseX * 0.001;
        targetY = mouseY * 0.001;
        
        particleSystem.rotation.y += 0.05 * (targetX - particleSystem.rotation.y);
        particleSystem.rotation.x += 0.05 * (targetY - particleSystem.rotation.x);
        
        // Continuous slow rotation
        particleSystem.rotation.y += 0.002;

        renderer.render(scene, camera);
    };

    animate();
};

window.addEventListener('DOMContentLoaded', init3DHeart);
