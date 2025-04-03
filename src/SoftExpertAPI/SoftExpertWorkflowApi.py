import base64
from .SoftExpertOptions import SoftExpertOptions
from .SoftExpertBaseAPI import SoftExpertBaseAPI
from .SoftExpertException import SoftExpertException

import xml.etree.ElementTree as ET


class SoftExpertWorkflowApi(SoftExpertBaseAPI):

    def __init__(self, options: SoftExpertOptions):
        super().__init__(options, "/apigateway/se/ws/wf_ws.php")  

    def _remove_namespace(self, xml):
            return xml.replace('xmlns="urn:workflow"', '')

    def newWorkflow(self, ProcessID:str , WorkflowTitle: str, UserID: str = None):
        """
        Cria um workflow
        """
        action = "urn:newWorkflow"

        xml_UserID = ""
        if(UserID != None):
            xml_UserID = f"<urn:UserID>{UserID}</urn:UserID>"
        
        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <!--You may enter the following 3 items in any order-->
                    <urn:ProcessID>{ProcessID}</urn:ProcessID>
                    <urn:WorkflowTitle>{WorkflowTitle}</urn:WorkflowTitle>

                    <!--Optional:-->
                    {xml_UserID}

                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        
        
        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        try:
           # Encontrando o RecordID
            record_id = root.find(".//RecordID").text
            return record_id
        
        except:
            Detail = root.find(".//Detail").text
            raise SoftExpertException.SoftExpertException(f"Resposta do SoftExpert: {Detail}")

       


       

        
    def executeActivity(self, WorkflowID: str, ActivityID: str, ActionSequence: int, UserID: str = None):
        """
        Executa uma atividade
        """
        action = "urn:executeActivity"

        xml_UserID = ""
        if(UserID != None):
            xml_UserID = f"<urn:UserID>{UserID}</urn:UserID>"
        
        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <!--You may enter the following 5 items in any order-->
                    <urn:WorkflowID>{WorkflowID}</urn:WorkflowID>
                    <urn:ActivityID>{ActivityID}</urn:ActivityID>
                    <urn:ActionSequence>{ActionSequence}</urn:ActionSequence>

                    <!--Optional:-->
                    {xml_UserID}
                    <!--Optional:-->
                    <urn:ActivityOrder></urn:ActivityOrder>

                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        Status = root.find(".//Status").text
        Detail = root.find(".//Detail").text
        if(Status == "FAILURE"):
            raise SoftExpertException.SoftExpertException(f"Resposta do SoftExpert: {Detail}")





       
    def editEntityRecord(self, WorkflowID: str, EntityID: str, form: dict, relationship: dict = None, files: dict = None):
        """
        Permite editar o formulário de uma instância

        Valor do atributo da tabela de formulário.
        Observações de acordo com o tipo do atributo:
        ▪ Número: dígitos numéricos sem separador de milhar e decimal
        ▪ Decimal: dígitos numéricos sem separador de milhar e com ponto (.) como separador decimal
        ▪ Data: YYYY-MM-DD
        ▪ Hora: HH:MM
        ▪ Boolean: 0 ou 1
        """

        action = "urn:editEntityRecord"
        xml_Form = ""
        for key, value in form.items():
            xml_Form += f"""
                <urn:EntityAttribute>
                    <urn:EntityAttributeID>{key}</urn:EntityAttributeID>
                    <urn:EntityAttributeValue>{value}</urn:EntityAttributeValue>
                </urn:EntityAttribute>
            """
        
        xml_Relationship = ""
        if(relationship != None):
            for key, value in relationship.items():
                for subkey, subvalue in value.items():
                    xml_Relationship += f"""
                        <urn:Relationship>
                            <urn:RelationshipID>{key}</urn:RelationshipID>
                            <urn:RelationshipAttribute>
                                <urn:RelationshipAttributeID>{subkey}</urn:RelationshipAttributeID>
                                <urn:RelationshipAttributeValue>{subvalue}</urn:RelationshipAttributeValue>
                            </urn:RelationshipAttribute>
                        </urn:Relationship>
                    """
        xml_Files = ""
        for key, value in files.items():
            for subkey, subvalue in value.items():
                xml_Files += f"""
                    <urn:EntityAttributeFile>
                        <urn:EntityAttributeID>{key}</urn:EntityAttributeID>
                        <urn:FileName>{subkey}</urn:FileName>
                        <urn:FileContent>{base64.b64encode(subvalue).decode()}</urn:FileContent>
                    </urn:EntityAttributeFile>
                """


        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <!--You may enter the following 5 items in any order-->
                    <urn:WorkflowID>{WorkflowID}</urn:WorkflowID>
                    <urn:EntityID>{EntityID}</urn:EntityID>
                    
                    <urn:EntityAttributeList>
                        {xml_Form}
                    </urn:EntityAttributeList>

                    <urn:RelationshipList>
                        {xml_Relationship}
                    </urn:RelationshipList>

                    <urn:EntityAttributeFileList>
                        {xml_Files}
                    </urn:EntityAttributeFileList>
                    
                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        Status = root.find(".//Status").text
        Detail = root.find(".//Detail").text
        if(Status == "FAILURE"):
            raise SoftExpertException.SoftExpertException(f"Resposta do SoftExpert: {Detail}", xml_body)
