function Ignore-SelfSignedCerts
{
   try
   {
       Write-Host "Adding TrustAllCertsPolicy type." -ForegroundColor White
       Add-Type -TypeDefinition  @"
       using System.Net;
       using System.Security.Cryptography.X509Certificates;
       public class TrustAllCertsPolicy : ICertificatePolicy
       {
            public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem)
            {
                return true;
           }
       }
"@
       Write-Host "TrustAllCertsPolicy type added." -ForegroundColor White
     }
   catch
   {
       Write-Host $_ -ForegroundColor "Yellow"
   }
   [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
}
Ignore-SelfSignedCerts
write-host ""

# Allow all secure protocols
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]'Ssl3,Tls,Tls11,Tls12'