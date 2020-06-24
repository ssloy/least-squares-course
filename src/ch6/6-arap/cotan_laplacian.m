function [cotWeight,cotLaplacian] = cotan_laplacian(V, T)

nf = size(T,1);
nv = size(V,1);

normv = @(V) sqrt(sum(V.^2,2));
E1 = V(T(:,2),:)-V(T(:,3),:);
L1 = normv(E1);
E2 = V(T(:,1),:)-V(T(:,3),:);
L2 = normv(E2);
E3 = V(T(:,1),:)-V(T(:,2),:);
L3 = normv(E3);

A1 = (L2.^2 + L3.^2 - L1.^2) ./ (2.*L2.*L3);
A2 = (L1.^2 + L3.^2 - L2.^2) ./ (2.*L1.*L3);
A3 = (L1.^2 + L2.^2 - L3.^2) ./ (2.*L1.*L2);
A = [A1,A2,A3];
A = acos(A);
cotWeight = abs(cot(A));

I = [T(:,1);T(:,2);T(:,3)];
J = [T(:,2);T(:,3);T(:,1)];
S = 0.5*abs(cot([A(:,3);A(:,1);A(:,2)]));
In = [I;J;I;J];
Jn = [J;I;I;J];
Sn = [-S;-S;S;S];
cotLaplacian = sparse(In,Jn,Sn,nv,nv);