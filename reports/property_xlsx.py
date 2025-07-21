from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval


class propertyxlsx(http.Controller):

    @http.route("/property/exel/report/<string:property_ids>", type="http",auth="user" )
    def download_property_xlsx(self,property_ids):
        property_ids = request.env['property'].browse(literal_eval(property_ids))
        print(property_ids)
        output=io.BytesIO()
        workbook=xlsxwriter.Workbook(output,options={'in_memory':True})
        workshet=workbook.add_worksheet('Properties')

        header_format=workbook.add_format({'bold':True,'bg_color': 'D3D3D3','border':1,'align':'center'})
        string_format=workbook.add_format({'border':1,'align':'center'})
        priceformat=workbook.add_format({'num_format':'$##,##00.00','border':1,'align':'center'})

        headers=['Name','Postcode','Selling Price','State','Bedrooms']
        for i,header in enumerate(headers):
            workshet.write(0,i,header,header_format)
        
        rw=1
        for prop in property_ids:
                workshet.write(rw,0,prop.name,string_format)
                workshet.write(rw,1,prop.postcode,string_format)
                workshet.write(rw,2,prop.selling_price,priceformat)
                workshet.write(rw,3,prop.state,string_format)
                workshet.write(rw,4,prop.bedrooms,string_format)
                rw+=1

        

        workbook.close()
        output.seek(0)


        file_name='property_report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('content-type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('content-dispositon',f'attachement; filename={file_name}')
            ]
        )