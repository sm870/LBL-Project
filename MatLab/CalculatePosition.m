function [P1,P2,solexist] = CalculatePosition(T1,T2,r1,r2)
    solexist = true;
    % Find solution in a coordinate system where T1 is (0,0) and T2 is (d12, 0) where d12 is the distance between the two beacons
    

    % Calculate d12
    d12 = norm(T1-T2);

    % Check is a solution exist
    if (r1+r2 >= d12)
        x = (d12^2-r2^2+r1^2)/(2*d12);
        y1 = sqrt(r1^2-x^2);
        y2 = -sqrt(r1^2-x^2);
    
    else
        solexist = false;
        return;
    end
    % Now convert solution in real world coordinates
    
    % First turn (x,y) by -angle between vector T1T2 and x axis in real world
    angle = atan2(T2(2)-T1(2),T2(1)-T1(1));
    % Creating rotation matrix
    R = [cos(angle) -sin(angle); sin(angle) cos(angle)];
    P1 = R*[x;y1] + T1;
    
    P2 = R*[x;y2] + T1;
end
