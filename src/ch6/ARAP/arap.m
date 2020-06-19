clear all; close all; clc;

[V,T] = readOBJ('diablo.obj');
nf = size(T,1);
nv = size(V,1);

id_lock = [1176; 1766; 382; 2384; 1779];
V_lock = V(id_lock,:) + [0,0,-0.5; 0,0,0.5; 0,0,-0.5; 0,0,0.5; 1.5,0,0];
id_free = setdiff((1:nv)', id_lock);

figure;
trisurf(T, V(:,1), V(:,2), V(:,3), 1);
hold on;
plot3(V(id_lock,1), V(id_lock,2), V(id_lock,3), 'xr');
quiver3(V(id_lock,1), V(id_lock,2), V(id_lock,3), V_lock(:,1)-V(id_lock,1), V_lock(:,2)-V(id_lock,2), V_lock(:,3)-V(id_lock,3), 0, 'r');
axis equal;

%% Compute cotangents Laplacian
[cotWeight,cotLaplacian] = cotan_laplacian(V, T);

U = zeros(nv,3);
U(id_lock,:) = V_lock - V(id_lock,:);
U(id_free,:) = cotLaplacian(id_free,id_free) \ ( - cotLaplacian(id_free,id_lock)*U(id_lock,:));

V_lap = V + U;

figure;
trisurf(T, V_lap(:,1), V_lap(:,2), V_lap(:,3), 1);
axis equal;

%% As-rigid-as possible
E1 = V(T(:,2),:) - V(T(:,3),:);
E2 = V(T(:,1),:) - V(T(:,3),:);
E3 = V(T(:,1),:) - V(T(:,2),:);
V_prime = V;
Rot = cell(nv,1);

tic;
maxIter = 200;
for i = 1:maxIter
    fprintf('Iteration %d... ',i);
    
    % Now, estimate the rotations
    E1new = V_prime(T(:,2),:) - V_prime(T(:,3),:);
    E2new = V_prime(T(:,1),:) - V_prime(T(:,3),:);
    E3new = V_prime(T(:,1),:) - V_prime(T(:,2),:);
    
    for j = 1:nv
        Rot{j} = zeros(3,3);
    end
    for j = 1:nf
        Rot{T(j,3)} = Rot{T(j,3)} + cotWeight(j,1)*E1(j,:)'*E1new(j,:);
        Rot{T(j,2)} = Rot{T(j,2)} + cotWeight(j,1)*E1(j,:)'*E1new(j,:);
        
        Rot{T(j,3)} = Rot{T(j,3)} + cotWeight(j,2)*E2(j,:)'*E2new(j,:);
        Rot{T(j,1)} = Rot{T(j,1)} + cotWeight(j,2)*E2(j,:)'*E2new(j,:);
        
        Rot{T(j,2)} = Rot{T(j,2)} + cotWeight(j,3)*E3(j,:)'*E3new(j,:);
        Rot{T(j,1)} = Rot{T(j,1)} + cotWeight(j,3)*E3(j,:)'*E3new(j,:);
    end
    for j = 1:nv
        [Usvd,~,Vsvd] = svd(Rot{j});
        Rot{j} = Vsvd * Usvd';
        
        if det(Rot{j}) < 0
            Vsvd(:,3)=-Vsvd(:,3);
			Rot{j} = Vsvd * Usvd';
        end
    end
    
    % Do linear solve for the vertex position
    e1Rot = zeros(nf,3);
    e2Rot = zeros(nf,3);
    e3Rot = zeros(nf,3);
    for j = 1:nf
        e1Rot(j,:) = 0.5*((Rot{T(j,2)} + Rot{T(j,3)})*E1(j,:)')';
        e2Rot(j,:) = 0.5*((Rot{T(j,1)} + Rot{T(j,3)})*E2(j,:)')';
        e3Rot(j,:) = 0.5*((Rot{T(j,1)} + Rot{T(j,2)})*E3(j,:)')';
    end
    
    e1Rot = bsxfun(@times,e1Rot,cotWeight(:,1));
    e2Rot = bsxfun(@times,e2Rot,cotWeight(:,2));
    e3Rot = bsxfun(@times,e3Rot,cotWeight(:,3));
    
    b = zeros(nv,3);
    o = ones(nf,1);
    for dim = 1:3
        b(:,dim) = b(:,dim) + accumarray([T(:,2) o], e1Rot(:,dim),[size(b,1) 1]);
        b(:,dim) = b(:,dim) + accumarray([T(:,3) o],-e1Rot(:,dim),[size(b,1) 1]);
        
        b(:,dim) = b(:,dim) + accumarray([T(:,1) o], e2Rot(:,dim),[size(b,1) 1]);
        b(:,dim) = b(:,dim) + accumarray([T(:,3) o],-e2Rot(:,dim),[size(b,1) 1]);
        
        b(:,dim) = b(:,dim) + accumarray([T(:,1) o], e3Rot(:,dim),[size(b,1) 1]);
        b(:,dim) = b(:,dim) + accumarray([T(:,2) o],-e3Rot(:,dim),[size(b,1) 1]);
    end
    b = 0.5*b;
    
    V_old = V_prime;
    V_prime(id_lock,:) = V_lock;
    V_prime(id_free,:) = cotLaplacian(id_free,id_free) \ (b(id_free,:) - cotLaplacian(id_free,id_lock)*V_lock);
    vertexChange = norm(V_prime(:) - V_old(:),'inf')/norm(V_prime,'inf');
    
    fprintf(' change = %g\n',vertexChange);
    if i > 5 && vertexChange < 1e-4 % .1% change
        break;
    end
end


figure;
trisurf(T, V_prime(:,1), V_prime(:,2), V_prime(:,3), 1);
axis equal;
