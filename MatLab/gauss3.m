Target = [700;700;700];
Noise = 10;
%positions of transponders
T1 = [1000;0;0];
T2 = [1000;1000;0];
T3 = [0;500;0];
T4 = [500;500;500];
T5 = [300;800;1000];
T6 = [100;300;300];
T7 = [200;400;800];
T8 = [600;450;650];


%T = [T1 T2 T3 T4 T5];
T = [T1 T2 T3 T4 T5 T6 T7 T8];
% measurements from target to transponders
M(1) = norm(T1-Target)+Noise*rand(1);
M(2) = norm(T2-Target)+Noise*rand(1);
M(3) = norm(T3-Target)+Noise*rand(1);
M(4) = 2*(norm(T4-Target)+Noise*rand(1));
M(5) = norm(T5-Target)+Noise*rand(1);
M(6) = norm(T6-Target)+Noise*rand(1);
M(7) = 2*(norm(T7-Target)+Noise*rand(1));
M(8) = norm(T8-Target)+Noise*rand(1);


tol = 1e-8; %set a value for the accuracy
maxstep = 100; %set maximum number of steps to run for


x = [100;100;100]; %set initial guess for origin
m=size(T,2); %determine number of measurments
n=size(T,1); %determine number of unknowns
xold = x;

% create figure;
%close all;
figure(1);
%origin(expect it to be 0,0)
title('Gauss-Newton Approximation of Data Points') %set axis
%lables, title and legend
xlabel('X')
ylabel('Y')
zlabel('Z')
plot3(T(1,:),T(2,:),T(3,:),'r*') %plot the data points
hold on;


for k=1:maxstep %iterate through process
% S = 0;
 for i=1:m
     d(i) = norm(T(:,i)-x);
     J(i,:) = (x-T(:,i))/d(i);
 end
 g = pinv(J');
 
 % Calculate residuals
 r = M-d;
 
 x = xold+g'*r'; %calculate new approximation
 err(k) = norm(x-xold); %calculate error
 if (abs(err(k)) <= tol); %if less than tolerance break
    break
 end
 xold=x
 steps = k;
plot3(x(1),x(2),x(3),'b*') %plot the approximation of the
legend('Data Points','Gauss-Newton Approximation of target','Location','north')
%pause;
end
k=k
