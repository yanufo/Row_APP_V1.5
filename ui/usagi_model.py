import base64
from pathlib import Path

import streamlit.components.v1 as components

GLB_PATH = "/models/usagi.glb"

def display_3d_usagi(
    height: int = 520,
    target_size: float = 9,
):
    """
    Display a GLB 3D model using Three.js inside Streamlit.

    Parameters
    ----------
    glb_path : str | Path
        Path to the GLB model.

    height : int
        Height of the Streamlit component.

    target_size : float
        Target size used to scale the model in the viewer.
    """

    glb_path = Path(glb_path)

    # ============================================================
    # Load GLB
    # ============================================================

    with open(glb_path, "rb") as f:
        glb_base64 = base64.b64encode(f.read()).decode("utf-8")

    # ============================================================
    # HTML / JavaScript
    # ============================================================

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>

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

    camera.position.set(7, 4.5, 7);


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

    renderer.setClearColor(0x000000, 0);

    // Three.js r128
    renderer.outputEncoding = THREE.sRGBEncoding;

    container.appendChild(renderer.domElement);


    // ============================================================
    // Lighting
    // ============================================================

    const ambient = new THREE.AmbientLight(
        0xffffff,
        0.8
    );

    scene.add(ambient);


    const light1 = new THREE.DirectionalLight(
        0xffffff,
        1.5
    );

    light1.position.set(10, 20, 10);

    scene.add(light1);


    const light2 = new THREE.DirectionalLight(
        0xffffff,
        0.8
    );

    light2.position.set(-10, 10, -10);

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
    // GLB
    // ============================================================

    const glbBase64 = "{glb_base64}";


    // ============================================================
    // Base64 → ArrayBuffer
    // ============================================================

    function base64ToArrayBuffer(base64) {{

        const binaryString = atob(base64);

        const len = binaryString.length;

        const bytes = new Uint8Array(len);

        for (let i = 0; i < len; i++) {{
            bytes[i] = binaryString.charCodeAt(i);
        }}

        return bytes.buffer;
    }}


    // ============================================================
    // Load GLB
    // ============================================================

    try {{

        const glbData = base64ToArrayBuffer(glbBase64);

        const loader = new THREE.GLTFLoader();


        loader.parse(
            glbData,
            "",
            function(gltf) {{

                const model = gltf.scene;

                scene.add(model);


                // ====================================================
                // Calculate model dimensions
                // ====================================================

                const box =
                    new THREE.Box3().setFromObject(model);

                const center =
                    box.getCenter(new THREE.Vector3());

                const size =
                    box.getSize(new THREE.Vector3());


                // ====================================================
                // Center model
                // ====================================================

                model.position.sub(center);


                // ====================================================
                // Scale model
                // ====================================================

                const maxSize =
                    Math.max(
                        size.x,
                        size.y,
                        size.z
                    );

                const targetSize = {target_size};

                const scale =
                    targetSize / maxSize;

                model.scale.setScalar(scale);


                // ====================================================
                // Camera
                // ====================================================

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

            }},

            function(error) {{

                console.error(error);

                document.getElementById("error").innerText =
                    "Error loading GLB: " +
                    error.message;

            }}
        );

    }}

    catch (error) {{

        console.error(error);

        document.getElementById("error").innerText =
            "Error loading 3D model: " +
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
        height=height,
    )