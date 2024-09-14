import React, { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stage, useFBX } from '@react-three/drei';
import modelPath from './../img/cat_galaxy.fbx';

const RotatingModel = () => {
    const modelRef = useRef();
    const fbx = useFBX(modelPath); // 모델 경로를 올바르게 수정해주세요

    // 매 프레임마다 모델 회전
    useFrame(() => {
        if (modelRef.current) {
            // modelRef.current.rotation.x += 0.01; // Y축을 기준으로 회전
            modelRef.current.rotation.y += 0.01; // Y축을 기준으로 회전
            // modelRef.current.rotation.z += 0.01; // Y축을 기준으로 회전
        }
    });

    // 모델을 원하는 크기로 조정
    fbx.scale.set(1, 1, 1);
    fbx.rotation.y = 0; // 기본 회전값

    // 컴포넌트 언마운트 시 리소스 해제
    useEffect(() => {
        return () => {
            fbx.traverse((child) => {
                if (child.isMesh) {
                    if (child.geometry) child.geometry.dispose(); // Geometry 해제
                    if (child.material) {
                        if (Array.isArray(child.material)) {
                            child.material.forEach((mat) => mat.dispose()); // Material 해제
                        } else {
                            child.material.dispose();
                        }
                    }
                }
            });
        };
    }, [fbx]);

    return (
        <group>
            {/* 회전축을 조정하려면 그룹을 사용하여 위치 조정 */}
            <mesh position={[0, 0, 0]} ref={modelRef}>
                <primitive object={fbx} />
            </mesh>
        </group>
    );
};

const ThreeScene = () => {
    const controlsRef = useRef();

    return (
        <Canvas>
            {/* OrbitControls 설정 */}
            <OrbitControls
                ref={controlsRef}
                enableDamping
                dampingFactor={0.1}
                rotateSpeed={0.5}
                minPolarAngle={Math.PI / 2} // 90도, 수직 회전 방지
                maxPolarAngle={Math.PI / 2} // 90도, 수직 회전 방지
                enableZoom={true}
                enablePan={true}
                enableRotate={true} // 회전 허용
            />
            <Stage>
                <RotatingModel />
            </Stage>
            <ambientLight intensity={0.5} />
            <directionalLight position={[10, 10, 10]} intensity={1} />

            {/* 컴포넌트 언마운트 시 리소스 정리 */}
            <UnmountCleanup controlsRef={controlsRef} />
        </Canvas>
    );
};

const UnmountCleanup = ({ controlsRef }) => {
    useEffect(() => {
        return () => {
            if (controlsRef.current) {
                controlsRef.current.dispose(); // OrbitControls 해제
            }
        };
    }, [controlsRef]);

    return null;
};

export default ThreeScene;

