import base64
from pathlib import Path

import streamlit.components.v1 as components

def display_3d_drone(
    height: int = 520,
    target_size: float = 9,
):
    OBJ_PATH = "/app/models/drone_costum.obj"

    with open(OBJ_PATH, "rb") as f:
        obj_base64 = base64.b64encode(f.read()).decode("utf-8")

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/OBJLoader.js"></script>

    <style>

    html, body {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: transparent;
    }}

    #viewer {{
        width: 100%;
        height: {height}px;
        background: transparent;
    }}

    canvas {{
        display: block;
    }}

    #error {{
        position: absolute;
        top: 20px;
        left: 20px;
        color: red;
        font-family: Arial;
        font-size: 16px;
    }}

    </style>

    </head>

    <body>

    <div id="viewer"></div>

    <div id="error"></div>


    <script>

    const container = document.getElementById("viewer");


    // ============================================================
    // Scene
    // ============================================================

    const scene = new THREE.Scene();

    scene.background = null;


    // ============================================================
    // Camera
    // ============================================================

    const camera = new THREE.PerspectiveCamera(
        45,
        container.clientWidth / container.clientHeight,
        0.01,
        100000
    );

    camera.position.set(
        6,
        4,
        6
    );


    // ============================================================
    // Renderer
    // ============================================================

    const renderer = new THREE.WebGLRenderer({{
        antialias: true,
        alpha: true
    }});

    renderer.setPixelRatio(window.devicePixelRatio);

    renderer.setSize(
        container.clientWidth,
        container.clientHeight
    );

    renderer.setClearColor(
        0x000000,
        0
    );

    container.appendChild(renderer.domElement);


    // ============================================================
    // Lighting
    // ============================================================

    const ambient = new THREE.AmbientLight(
        0xffffff,
        2.5
    );

    scene.add(ambient);


    const light1 = new THREE.DirectionalLight(
        0xffffff,
        4
    );

    light1.position.set(
        10,
        20,
        10
    );

    scene.add(light1);


    const light2 = new THREE.DirectionalLight(
        0xffffff,
        2
    );

    light2.position.set(
        -10,
        10,
        -10
    );

    scene.add(light2);


    // ============================================================
    // Controls
    // ============================================================

    const controls = new THREE.OrbitControls(
        camera,
        renderer.domElement
    );

    controls.enableDamping = true;

    controls.dampingFactor = 0.05;

    controls.enablePan = true;

    controls.enableZoom = true;

    controls.minDistance = 1;

    controls.maxDistance = 100;


    // ============================================================
    // OBJ
    // ============================================================

    const objBase64 = "{obj_base64}";

    // Python parameter passed into JavaScript
    const targetSize = {target_size};


    function base64ToString(base64) {{

        const binary = atob(base64);

        const bytes = new Uint8Array(
            binary.length
        );

        for (
            let i = 0;
            i < binary.length;
            i++
        ) {{
            bytes[i] =
                binary.charCodeAt(i);
        }}

        return new TextDecoder().decode(bytes);
    }}


    // ============================================================
    // Load Drone
    // ============================================================

    try {{

        const objText =
            base64ToString(objBase64);

        const loader =
            new THREE.OBJLoader();

        const drone =
            loader.parse(objText);


        // ========================================================
        // Material
        // ========================================================

        drone.traverse(function(child) {{

            if (child instanceof THREE.Mesh) {{

                child.material =
                    new THREE.MeshStandardMaterial({{
                        color: 0xB22222,
                        roughness: 0.45,
                        metalness: 0.5
                    }});

                child.castShadow = true;
                child.receiveShadow = true;
            }}

        }});


        scene.add(drone);


        // ========================================================
        // Get dimensions
        // ========================================================

        const box =
            new THREE.Box3().setFromObject(drone);

        const center =
            box.getCenter(
                new THREE.Vector3()
            );

        const size =
            box.getSize(
                new THREE.Vector3()
            );


        // ========================================================
        // Center
        // ========================================================

        drone.position.sub(center);


        // ========================================================
        // Scale Model
        // ========================================================

        const maxSize =
            Math.max(
                size.x,
                size.y,
                size.z
            );

        const scale =
            targetSize / maxSize;

        drone.scale.setScalar(scale);


        // ========================================================
        // Camera
        // ========================================================

        camera.position.set(
            7,
            4.5,
            7
        );

        camera.lookAt(
            0,
            0,
            0
        );

        controls.target.set(
            0,
            0,
            0
        );

        controls.update();


    }} catch (error) {{

        console.error(error);

        document.getElementById(
            "error"
        ).innerText =
            "Error loading drone: " +
            error.message;

    }}


    // ============================================================
    // Resize
    // ============================================================

    window.addEventListener(
        "resize",
        function() {{

            camera.aspect =
                container.clientWidth /
                container.clientHeight;

            camera.updateProjectionMatrix();

            renderer.setSize(
                container.clientWidth,
                container.clientHeight
            );

        }}
    );


    // ============================================================
    // Animation
    // ============================================================

    function animate() {{

        requestAnimationFrame(animate);

        controls.update();

        renderer.render(
            scene,
            camera
        );

    }}

    animate();

    </script>

    </body>

    </html>
    """

    components.html(
        html,
        height=height
    )