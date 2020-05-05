clc; clear all; close all
EQ_List={'RSN1087_NORTHR_TAR360.AT2',... 
        'RSN1231_CHICHI_CHY080-E.AT2',...
        'RSN1231_CHICHI_CHY080-N.AT2',...
        'RSN1605_DUZCE_DZC180.AT2',...
        'RSN1605_DUZCE_DZC270.AT2',...
        'RSN214_LIVERMOR_A-KOD180.AT2',...
        'RSN214_LIVERMOR_A-KOD270.AT2',...
        'RSN230_MAMMOTH.I_I-CVK090.AT2',...
        'RSN230_MAMMOTH.I_I-CVK180.AT2',...
        'RSN292_ITALY_A-STU000.AT2',...
        'RSN292_ITALY_A-STU270.AT2',...
        'RSN558_CHALFANT.A_A-ZAK270.AT2',...
        'RSN558_CHALFANT.A_A-ZAK360.AT2',...
        'RSN614_WHITTIER.A_A-BIR090.AT2',...
        'RSN614_WHITTIER.A_A-BIR180.AT2',...
        'RSN95_MANAGUA_A-ESO090.AT2',...
        'RSN95_MANAGUA_A-ESO180.AT2',...
        'RSN982_NORTHR_JEN022.AT2',...
        'RSN982_NORTHR_JEN292.AT2'};

dt_list=[0.02,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.0024,0.0024,0.005,0.005,0.005,0.005,0.005,0.005,0.005,0.005];


% ======================== Program ESPECTRO.m =========================== %

%    Program for the analysis of strong motion data, it calculates:

%    - velocity and displacement time histories by trapezoidal integration

%    - Fourier spectrum via FFT

%    - Displacement, pseudo-velocity and pseudo-acceleration response
%      spectrum for any values of damping ratio. Equation of motion is
%      solved using the duhamel integral.

%    - Husid plot, significant duration and bracketed duration

%               LUIS A. MONTEJO (lumontv@yahoo.com.ar)

%         uptades available at www.geocities.com/lumontv/eng

%      DEPARTMENT OF CIVIL, CONSTRUCTION AND ENVIROMENTAL ENGINEERING

%                  NORTH CAROLINA STATE UNIVERSITY

%                       last updated: 02/20/2007

% ======================================================================= %

neq=length(EQ_List);

for i=1:neq
    % Input data:
    clearvars -except EQ_List neq dt_list i
    name =char(EQ_List(i)) ;                                % identifies actual work, the output file will be name.xls

    dt   = dt_list(i);                                  % time step of accelerogram [sec]
    zi   = [0.05];                    % vector with the damping ratios
    nom  = char(EQ_List(i));                                % name of earthquake file
    go   = 1;                                     % acceleration of gravity in the same untis that
                                                  % your eq. record is, ig your record is in g's
                                                  % then input 1

    Tmax = 10;			                          % final period for spectra [sec]
    Ti   = 0.001;                                 % initial period for spectra [sec]
    dT   = 0.1; 
    % interval for natural periods


    % ==============================================================
    % ============================================ END OF INPUT DATA
































    % ========================================================================
     % ========================================================================



    nzi  = length(zi);                      % number of damping ratios
    g    = 981;                             % acceleration of gravity [cm/s^2]
    addpath('C:\ConditionDependent_PBD\EarthquakeSelection\Mainshock_Test_g3files');            % directory with the accelerograms
    terr = load ([nom,'.g3']);             % read earthquake data file
    [nr,nc]  = size(terr); 	                % columns and rows of data file
    nt       = nr*nc;		     		    % original number of data points
    xg(1:nt) = (g/go)*terr';                % copy accelerogram in a vector
    np = length(xg);
    Tu   = (np-1) * dt;	    	        % final time of accelerogram
    t    = 0: dt: Tu;				        % vector with sampled times

    %==========================================================================
    %========== velocities and displacements via trapezoidal integration:

    vel   = dt*cumtrapz(xg);
    despl = dt*cumtrapz(vel); 

    figure;subplot(3,1,1); plot( t,xg/g, 'b','LineWidth',1); 
    grid on; axis tight; 
    title(['acceleration, velocity and displacement time histories for ',nom],'FontSize',16);
    ylabel('accel. [%g]','FontSize',16);

    subplot(3,1,2); plot( t,vel,'b', 'LineWidth',1); grid on;
    axis tight; ylabel('vel. [cm/s]','FontSize',16);

    subplot(3,1,3); plot( t,despl,'b' ,'LineWidth',1); grid on;
    axis tight; xlabel('time [s]','FontSize',16); ylabel('displ. [cm]','FontSize',16);

    %==========================================================================
    %========== response spectrum via Duhamel integral:

    T    = Ti: dT: Tmax;     	                  % vector with natural periods

    nper   = length(T);						          % number of natural periods
    SD     = zeros(nzi,nper);				          % rel. displac. spectrum
    PSV    = zeros(nzi,nper);				          % pseudo-vel. spectrum
    PSA    = zeros(nzi,nper);				          % pseudo-acc. spectrum

    for k = 1 : nzi
        for j = 1 : nper
            wn       = 2*pi/T(j);
            ub       = duhamel(wn,zi(k),1,dt,nt,0,0,-xg);
            SD(k,j)    = max( abs(ub) );
        end
        PSV(k,:) = (2*pi./T) .* SD(k,:);                   % pseudo-vel. spectrum
        PSA(k,:) = (2*pi./T).^2 .* SD(k,:);  	          % pseudo-accel. spectrum
    end

    figure; plot(T,SD); grid on; axis tight;title(['Displacement Spectrum of ',nom],'FontSize',16);
    ylabel('displacement [cm]','FontSize',16); xlabel('period [s]','FontSize',16);

    figure; plot(T,PSV); grid on; axis tight;title(['Pseudo-Velocity Spectrum of ',nom],'FontSize',16);
    ylabel('PSV [cm/s]','FontSize',16); xlabel('period [s]','FontSize',16);

    figure; plot(T,PSA./g); grid on; axis tight;title(['Pseudo-Acceleration Spectrum of ',nom],'FontSize',16);
    ylabel('PSA [g]','FontSize',16); xlabel('period [s]','FontSize',16);


    %==========================================================================
    %============= Husid plot, significant duration:

    Ia = zeros(1,nt);
    for n = 1 : nt
        Ia(n) = pi/(2*g)*dt*trapz( xg(1:n).^2 );
    end
    AI  = Ia(np);
    Ia  = Ia/Ia(np);
    x1  = 0.05*ones(1,np);
    x2  = 0.95*ones(1,np);
    [xmin,imin] = min( abs(Ia-0.05) );
    [xmax,imax] = min( abs(Ia-0.95) );
    dur = t(imax) - t(imin);

    figure;  plot( t,Ia, t,x1, t,x2, t(imin),Ia(imin),'o', t(imax),Ia(imax),'o','LineWidth',2,...
                    'MarkerEdgeColor','m',...
                    'MarkerSize',8);
    grid on; axis tight; title(['Husid plot of ',nom],'FontSize',16);
    xlabel('Time [s]','FontSize',16); ylabel('Normalized intensity','FontSize',16);
    text(2,0.07,'5%','FontSize',16); text(2,0.97,'95%','FontSize',16); 
    text(Tu/2.7,0.55,['significant duration: ',num2str(dur),' s'],'FontSize',16)

    pc=find(abs(xg/g)>0.05);
    last=length(pc);
    tc1=t(pc(1)); acc1 = xg(pc(1)); 
    tc2=t(pc(last)); acc2 = xg(pc(last));
    duration=tc2-tc1;

    cs=ones(1,np);
    cs=0.05.*cs;

    figure;plot( t,abs(xg/g), 'b',t,cs,'r',tc1,abs(acc1)/g,'o',tc2,abs(acc2)/g,'o','LineWidth',1,...
                    'MarkerEdgeColor','r',...
                    'MarkerSize',8); 
    grid on; axis tight; 
    title(['bracketed duration of ',nom],'FontSize',16);
    ylabel('abs(accel.) [%g]','FontSize',16);xlabel('Time [s]','FontSize',16);
    text(Tu/2.5,0.95*max(abs(xg))/g,['bracketed duration: ',num2str(duration),' s'],'FontSize',16)

    %==========================================================================
    %============= Fourier spectrum via FFT:


    wny = pi/dt;					          % Nyquist frequency: rad/sec
    dw  = 2*pi / Tu;                          % frequency interval: rad/sec
    w   = 0.00001: dw: nt/2*dw;               % vector with frequencies in rad/sec
    f   = w/(2*pi);                           % vector with frequencies in cycles/sec                  
    Amp = dt * abs( fft(xg) );                % calculate the FT of the earthquake
    Amp = Amp(1:length(f));

    figure; plot( f, Amp ); grid on; 
    axis tight; title(['Fourier spectrum of ',nom],'FontSize',16)
    xlabel('Frequency f [Hz]','FontSize',16); ylabel('Amplitude','FontSize',16);

    % =========================================================================
    % =========================================================================


    THS = [t' xg'./g vel' despl' Ia'];
    PGA = max(abs(xg./g));
    PGV = max(abs(vel));
    PGD = max(abs(despl));


    fid = fopen([name,'.csv'],'w');

    fprintf(fid, ' \n');
    fprintf(fid, 'PGA:,  %4.2f g\n',PGA);
    fprintf(fid, 'PGV:,  %4.2f cm/s\n',PGV);
    fprintf(fid, 'PGD:,  %4.2f cm\n',PGD);
    fprintf(fid, 'Arias Intensity:,  %5.2f cm/s\n',AI);
    fprintf(fid, 'Significant duration:,  %5.2f s\n',dur);
    fprintf(fid, 'Bracketed  duration:,  %5.2f s\n',duration);
    fprintf(fid, ' \n');
    for k =1:nzi
        res = [T'  SD(k,:)'  PSV(k,:)'  PSA(k,:)'/g];
        fprintf(fid, ' \n');
        fprintf(fid, 'Damping ratio for spectra:  %3.2f\n\n',zi(k));
        fprintf(fid, ' \n');
        fprintf(fid, 'period [s]\tSD. [cm]\tPSV [cm/s]\tPSA [g]\n'); 
        fprintf(fid, '%3.4f\t, %4.3f\t, %4.3f\t, %4.3f\n',res');
        fprintf(fid, ' \n');

    end
    fprintf(fid, 'acceleration, velocity, displacement and normalized Arias intensity time histories:\n');
    fprintf(fid, ' \n');
    fprintf(fid, 'time [s]\taccel. [g]\tvel. [cm/s]\tdispl. [cm]\tAI\n'); 
    fprintf(fid, '%3.3f\t%1.7f\t%4.7f\t%4.7f\t%1.7f\n',THS');
    fprintf(fid, ' \n');
    fclose(fid);
end