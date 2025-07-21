from odoo import http
from odoo.http import request
from urllib.parse import parse_qs
import json
import math

#creating = post(status201)
#updating = put(status201)

def valid_response(data,status,pagination_info=None):
    response={
        'data':data
    }
    if pagination_info:
        response['pagination_info']=pagination_info

    return request.make_json_response(response,status=status)


def invalid_response(err):
    return request.make_json_response({
                    "ERROR":err,
                },status=400)


class PropertyApi(http.Controller):


    # @http.route("/v1/property" , methods=["POST"],type="http",auth="none",csrf=False)
    # def post_property(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     if not vals.get('name'):
    #         return invalid_response({
    #             "message":"WARNING : name is a required field",
    #         })
    #     try:
    #         res = request.env['property'].sudo().create(vals)
    #         if res:
    #             return valid_response({
    #                 "message":"Property Created Successfully",
    #                 "id":res.id,
    #                 "name":res.name
    #             },status=201)
    #     except Exception as err:
    #         return invalid_response({
    #             "message":err,
    #         })   
        
    
    @http.route("/v1/property" , methods=["POST"],type="http",auth="none",csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return invalid_response({
                "message":"WARNING : name is a required field",
            })
        try:
            colums=', '.join(vals.keys())
            values=', '.join(['%s']* len(vals)) 
            cr = request.env.cr
            query=f"""insert into property ({colums}) values ({values}) returning id,name,postcode;"""
            cr.execute(query,tuple(vals.values())) 
            res = cr.fetchone()
            print(res)
            if res:
                return valid_response({
                    "message":"Property has been Created Successfully",
                    "id":res[0],
                    "name":res[1],
                    "postcode":res[2],
                },status=201)
        except Exception as err:
            return invalid_response({
                "message":err,
            })   
        
    # @http.route("/v1/property/json" , methods=["POST"],type="json",auth="none",csrf=False)
    # def post_property_json(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     res = request.env['property'].sudo().create(vals)
    #     if res:
    #         return request.make_json_response([{
    #             "message":"Property Created Successfully"
    #         }])
        
    @http.route("/v1/property/<int:property_id>" , methods=["PUT"],type="http",auth="none",csrf=False)
    def update_property(self,property_id):
        try:
            property_id=request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return invalid_response({
                "message":"WARNING : Property_id missing",
                })

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return valid_response([{
                    "message":"Property Updated Successfully",
                    "id":property_id.id,
                    "name":property_id.name
                }],status=200)
        except Exception as err:
            return invalid_response({
                "message":err,
            })   
        

    @http.route("/v1/property/<int:property_id>" , methods=["GET"],type="http",auth="none",csrf=False)
    def read_property(self,property_id):
        try:
            property_id=request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return invalid_response({
                "message":"WARNING : Property_id missing",
                })

            return valid_response([{
                    "id":property_id.id,
                    "name":property_id.name,
                    "ref":property_id.ref,
                    "postcode":property_id.postcode,
                    "bedrooms":property_id.bedrooms,
                    "garden":property_id.garden,
                    "owner":property_id.owner_id.name,

                }],status=200)
        except Exception as err:
            return invalid_response({
                "message":err,
            })   

    @http.route("/v1/property/<int:property_id>" , methods=["DELETE"],type="http",auth="none",csrf=False)
    def delete_property(self,property_id):
        try:
            property_id=request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return invalid_response({
                "message":"WARNING : Property_id missing",
                })
            
            property_id.unlink()
            return valid_response({
            "message":"Property Record has been deleted",
            },status=200)
        
        except Exception as err:
            return invalid_response({
                "message":err,
            })    
 

    @http.route("/v1/properties" , methods=["GET"],type="http",auth="none",csrf=False)
    def get_list_of__property(self):
        try:
            property_domain=[]
            limit= 5
            page = offset= None

            param = parse_qs(request.httprequest.query_string.decode('utf-8'))

            if param.get('state'):
                property_domain += [('state','=',param.get('state')[0])]
            if param.get('limit'):
                limit=int(param.get('limit')[0])
            if param.get('page'):
                page=int(param.get('page')[0])
                if page : 
                    offset = (page*limit) - limit
        

            property_ids=request.env['property'].sudo().search(property_domain , offset=offset ,limit=limit, order='id desc')
            property_count=request.env['property'].sudo().search_count(property_domain)
            
            if not property_ids:
                return invalid_response({
                "message":"WARNING : There is no Record",
                })

            return valid_response([{
                    "id":prop.id,
                    "name":prop.name,
                    "ref":prop.ref,
                    "postcode":prop.postcode,
                    "bedrooms":prop.bedrooms,
                    "garden":prop.garden,
                    "owner":prop.owner_id.name,

                } for prop in property_ids]
                ,pagination_info={
                    'page':page if page else 1,
                    'limit':limit,
                    'pages':math.ceil(property_count/limit) if limit else 1,
                    'count':property_count,
                }
                ,status=200)
        
        except Exception as err:
            return invalid_response({
                "message":err,
            })     
        

