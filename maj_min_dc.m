% MAJ_MIN_DC Decomposition of non-DC MT into Major and Minor DC MTs.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Decompose seismic non-DC MT into Major and Minor DC MTs with preserved
% dominant eigenvector (P- or T-axis).
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Author: Miroslav HALLO
% Charles University in Prague, Faculty of Mathematics and Physics
% E-mail: hallo@karel.troja.mff.cuni.cz
% Revision 2017/02: The first version of the function
% Revision 2018/12: Enhanced version
% Revision 2026/04: New Matlab version
% Tested in Matlab R2025b
% Method:
% Hallo,M., Asano,K., Gallovic,F. (2017): Bayesian inference and interpretation
%      of centroid moment tensors of the 2016 Kumamoto earthquake sequence,
%      Kyushu, Japan, Earth, Planets and Space, 69:134.
%      https://doi.org/10.1186/s40623-017-0721-4
% Hallo,M., Oprsal,I., Asano,K., Gallovic,F. (2019): Seismotectonics of the 2018
%      Northern Osaka M6.1 earthquake and its aftershocks: joint movements
%      on strike-slip and reverse faults in inland Japan, Earth,
%      Planets and Space, 71:34. https://doi.org/10.1186/s40623-019-1016-8
%
% Copyright (C) 2017,2018 Miroslav Hallo
%
% This program is published under the GNU General Public License (GNU GPL).
%
% This program is free software: you can modify it and/or redistribute it
% or any derivative version under the terms of the GNU General Public
% License as published by the Free Software Foundation, either version 3
% of the License, or (at your option) any later version.
%
% This code is distributed in the hope that it will be useful, but WITHOUT
% ANY WARRANTY. We would like to kindly ask you to acknowledge the authors
% and don't remove their names from the code.
%
% You should have received copy of the GNU General Public License along
% with this program. If not, see <http://www.gnu.org/licenses/>.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INIT:
close all;
clearvars;
projRoot = fileparts(which(mfilename));
addpath(fullfile(projRoot, 'lib'));
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% INPUT:

% ASCII text file with Moment Tensors in Harvard notation (GCMT format)
% [Mrr, Mtt, Mpp, Mrt, Mrp, Mtp, Text]
% Note: Input components can be in normalized units (arbitrary scale).
% The decomposition preserves relative ratios, not absolute seismic moments.
mt_file = 'example_mt.txt';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Create directory for results
resDir = fullfile(projRoot, 'results');
if ~exist(resDir, 'dir')
    mkdir(resDir);
end

% Read file with Moment Tensors
try
    fid = fopen(mt_file,'r');
    mtlist = textscan(fid,'%f %f %f %f %f %f %[^\n]', 'CommentStyle', '#');
    fclose(fid);
catch
    mtlist = [];
end
total = length(mtlist{1,1});

% For each event
for eve = 1:total
    % Full Moment Tensor
    MT = zeros(1,6);
    for k = 1:6
        MT(k) = mtlist{1,k}(eve);
    end

    % Text label
    eve_name = mtlist{1,7}{eve};
    eve_name = regexprep(eve_name, '\s+', '_');
    eve_name = regexprep(eve_name, '[^\w]', '');
    if ~isempty(eve_name)
        eve_name = strcat(eve_name, '_');
    end

    % Convert MT from Harvard (GCMT) to Aki & Richards notation
    [MTa] = hrv2ar(MT);

    % Figure of full input MT
    figure('color','w')
    plotBB(MTa);
    title('Input full MT', 'FontWeight', 'normal')
    axis equal
    axis off

    % Save figure
    exportgraphics(gcf, fullfile(resDir, [eve_name,'input_MT_full.png']), ...
        'Resolution', 300)

    % 3x3 matrix (Aki & Richards notation)
    MT3 = [
        MTa(1), MTa(4), MTa(5);
        MTa(4), MTa(2), MTa(6);
        MTa(5), MTa(6), MTa(3)
        ];

    % Remove ISO
    Trace = trace(MT3) / 3;
    ISO = Trace / max(abs(eig(MT3)));
    MT3 = MT3 - diag([Trace Trace Trace]);

    % Figure of input deviatoric MT
    figure('color','w')
    plotBB([MT3(1,1), MT3(2,2), MT3(3,3), MT3(1,2), MT3(1,3), MT3(2,3)]);
    title('Input deviatoric MT', 'FontWeight', 'normal')
    axis equal
    axis off

    % Save figure
    exportgraphics(gcf, fullfile(resDir, [eve_name,'input_MT_deviatoric.png']), ...
        'Resolution', 300)

    % Eigenvalues and eigenvectors
    [V, D] = eig(MT3);

    % Sort eigenvalues and eigenvectors
    Lvect = [D(1,1), D(2,2), D(3,3)];
    disp('--------------------------------')
    disp('Non-DC MT eigenvalues:')
    disp(num2str(Lvect))
    disp(' ')
    [L,Li] = sort(abs(Lvect),'descend');
    La1 = D(Li(1), Li(1)); % Lambda 1
    La2 = D(Li(2), Li(2)); % Lambda 2
    La3 = D(Li(3), Li(3)); % Lambda 3
    v1 = V(:, Li(1)); % Eigenvector 1
    v2 = V(:, Li(2)); % Eigenvector 2
    v3 = V(:, Li(3)); % Eigenvector 3

    % Major and Minor DC MTs
    MTmaj = La2*(- v1*v1' + v2*v2'); % Major DC
    MTmin = La3*(- v1*v1' + v3*v3'); % Minor DC

    % Open text file for results
    fid = fopen(fullfile(resDir, [eve_name,'results.txt']),'w');

    % Display decomposed MT in Harvard notation
    disp('--------------------------------')
    disp('Input deviatoric MT (Harvard):')
    [mt_tmp(1),mt_tmp(2),mt_tmp(3),mt_tmp(4),mt_tmp(5),mt_tmp(6)] = ar2hrv(MT3);
    disp(num2str(mt_tmp))
    fprintf(fid,'%s\r\n','# Input deviatoric MT (Harvard):');
    fprintf(fid,'%9.6f  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f\r\n', mt_tmp);
    disp(' ')
    disp('Major DC MT (Harvard):')
    [mt_tmp(1),mt_tmp(2),mt_tmp(3),mt_tmp(4),mt_tmp(5),mt_tmp(6)] = ar2hrv(MTmaj);
    disp(num2str(mt_tmp))
    fprintf(fid,'%s\r\n','# Major DC MT (Harvard):');
    fprintf(fid,'%9.6f  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f\r\n', mt_tmp);
    disp(' ')
    disp('Minor DC MT (Harvard):')
    [mt_tmp(1),mt_tmp(2),mt_tmp(3),mt_tmp(4),mt_tmp(5),mt_tmp(6)] = ar2hrv(MTmin);
    disp(num2str(mt_tmp))
    fprintf(fid,'%s\r\n','# Minor DC MT (Harvard):');
    fprintf(fid,'%9.6f  %9.6f  %9.6f  %9.6f  %9.6f  %9.6f\r\n', mt_tmp);
    disp(' ')

    % Decompose Full, Major, and Minor MTs to DC
    [Dips0,Strikes0,Rakes0,VOL0,CLVD0,DC0,MDev0] = Decomposition(MT3);
    [Dips1,Strikes1,Rakes1,VOL1,CLVD1,DC1,MDev1] = Decomposition(MTmaj);
    [Dips2,Strikes2,Rakes2,VOL2,CLVD2,DC2,MDev2] = Decomposition(MTmin);

    % Display Full, Major, and Minor DC results
    disp('--------------------------------')
    disp('Input deviatoric MT (Strike/Dip/Rake):')
    disp(num2str([Strikes0(1), Dips0(1), Rakes0(1)],'%6.1f '))
    disp(num2str([Strikes0(2), Dips0(2), Rakes0(2)],'%6.1f '))
    disp(' ')
    disp('Major DC (Strike/Dip/Rake):')
    disp(num2str([Strikes1(1), Dips1(1), Rakes1(1)],'%6.1f '))
    disp(num2str([Strikes1(2), Dips1(2), Rakes1(2)],'%6.1f '))
    disp(' ')
    disp('Minor DC (Strike/Dip/Rake):')
    disp(num2str([Strikes2(1), Dips2(1), Rakes2(1)],'%6.1f '))
    disp(num2str([Strikes2(2), Dips2(2), Rakes2(2)],'%6.1f '))
    disp(' ')

    % Save Full, Major, and Minor DC results
    fprintf(fid,'%s\r\n','# Input deviatoric MT (Strike/Dip/Rake):');
    fprintf(fid,'%6.2f  %6.2f  %6.2f\r\n', Strikes0(1), Dips0(1), Rakes0(1));
    fprintf(fid,'%6.2f  %6.2f  %6.2f\r\n', Strikes0(2), Dips0(2), Rakes0(2));
    fprintf(fid,'%s\r\n','# Major DC (Strike/Dip/Rake):');
    fprintf(fid,'%6.2f  %6.2f  %6.2f\r\n', Strikes1(1), Dips1(1), Rakes1(1));
    fprintf(fid,'%6.2f  %6.2f  %6.2f\r\n', Strikes1(2), Dips1(2), Rakes1(2));
    fprintf(fid,'%s\r\n','# Minor DC (Strike/Dip/Rake):');
    fprintf(fid,'%6.2f  %6.2f  %6.2f\r\n', Strikes2(1), Dips2(1), Rakes2(1));
    fprintf(fid,'%6.2f  %6.2f  %6.2f\r\n', Strikes2(2), Dips2(2), Rakes2(2));

    % Ratio of scalar moments of Major and Minor DC MTs
    Cdc1 = max(abs(eig(MTmaj)));
    Cdc2 = max(abs(eig(MTmin)));
    N = Cdc1 + Cdc2;
    Cdc1 = Cdc1 / N;
    Cdc2 = Cdc2 / N;
    disp('Scalar seismic moment ratio of Major and Minor DC MTs:')
    disp([num2str(Cdc1*100,'%5.1f'),'% vs ', num2str(Cdc2*100,'%5.1f'), '%'] )

    % Save ratio of scalar moments
    fprintf(fid,'%s\r\n','# Scalar seismic moment ratio of Major and Minor DC MTs:');
    fprintf(fid,'%6.5f  %6.5f\r\n', Cdc1, Cdc2);
    
    % Close text file for results
    fclose(fid);

    % Plot Major and Minor MT
    figure('color','w')
    subplot(1,3,1)
    bb([Strikes1(1) Dips1(1) Rakes1(1)], 0.5, 0.5, Cdc1/2, 0, 'k')
    title('Major DC', 'FontWeight', 'normal')
    axis equal
    set(gca,'XLim',[0 1])
    set(gca,'YLim',[0 1])
    axis off

    subplot(1,3,2)
    bb([Strikes2(1) Dips2(1) Rakes2(1)], 0.5, 0.5, Cdc2/2, 0, 'k')
    title('Minor DC', 'FontWeight', 'normal')
    axis equal
    set(gca,'XLim',[0 1])
    set(gca,'YLim',[0 1])
    axis off

    subplot(1,3,3)
    plotBBclear([MT3(1,1),MT3(2,2),MT3(3,3),MT3(1,2),MT3(1,3),MT3(2,3)]);
    title('Deviatoric non-DC', 'FontWeight', 'normal')
    axis equal
    axis off

    % Save figure
    exportgraphics(gcf, fullfile(resDir, [eve_name,'trinity_MT_bb.png']), ...
        'Resolution', 300)

    % Close figures
    close all;
end

