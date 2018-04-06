function [sol,solexist] = Range(T1,T2,T3,Target,Noise)


r1 = norm(T1-Target)+Noise*rand(1);
r2 = norm(T2-Target)+Noise*rand(1);
r3 = norm(T3-Target)+Noise*rand(1);

[P1,P2,solexist] = CalculatePosition(T1,T2,r1,r2)
[P3,P4,solexist] = CalculatePosition(T1,T3,r1,r3)
[P5,P6,solexist] = CalculatePosition(T2,T3,r2,r3)

posvalues= [P1,P2,P3,P4,P5,P6];
sol1=[1,0,0,0,0,0];
for v = 3:1:6
    if ((P1(1)/posvalues(1,v))*100>=90 && (P1(1)/posvalues(1,v)*100)<=110)
        if ((P1(2)/posvalues(2,v))*100>=90 && (P1(2)/posvalues(2,v)*100)<=110)
            sol1(v)=1;
            
        end
    end
end

posvalues2= [P1,P2,P3,P4,P5,P6];
sol2=[0,1,0,0,0,0];
for v = 3:1:6
    if ((P2(1)/posvalues2(1,v))*100>=90 && (P2(1)/posvalues2(1,v)*100)<=110)
        if ((P2(2)/posvalues2(2,v))*100>=90 && (P2(2)/posvalues2(2,v)*100)<=110)
            sol2(v)=1;
        end
    end
end
solv = [0,0,0,0,0,0;0,0,0,0,0,0];
if ((sol1(1)+sol1(2)+sol1(3)+sol1(4)+sol1(5)+sol1(6))==3)
    for v=1:1:6
        solv(1,v)=sol1(v)*posvalues(1,v)
        solv(2,v)=sol1(v)*posvalues(2,v)
    end
else
    for v=1:1:6
        solv(1,v)=sol2(v)*posvalues2(1,v)
        solv(2,v)=sol2(v)*posvalues2(2,v)
    end
end
    % %plot(P1(1),P1(2),'+m',P2(1),P2(2),'+m');
% %plot(P3(1),P3(2),'+r',P4(1),P4(2),'+r');
% %plot(P5(1),P5(2),'+b',P6(1),P6(2),'+b');
sol(1) = ((solv(1,1)+solv(1,2)+solv(1,3)+solv(1,4)+solv(1,5)+solv(1,6))/3);
sol(2) = ((solv(2,1)+solv(2,2)+solv(2,3)+solv(2,4)+solv(2,5)+solv(2,6))/3);


end

