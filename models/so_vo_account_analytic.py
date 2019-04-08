# -*- coding: utf-8 -*-
 
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)
# alias construction = construction_contracting_change_order
class construction_change_order_extend(models.Model):
	_inherit = 'construction.change.order'

	@api.multi
	def done_state(self):
		_logger.critical('done_state')
		_logger.critical(self)
		budget_obj = self.env['so_vo.budget_change'].create({
				'contract_id':self.analytic_account_id.id,
				'name':self.name,
				'types':'Variation order',
				'reqstr_id':self.user_id.id,
				'apprvr_id':self.approve_by.id,
				'date_apprv':self.approve_date,
				'old_amount':self.original_contract_amount,
				'new_amount':self.total_contract_amount_all_change
			})
		res = super(construction_change_order_extend,self).done_state()

	# @api.model
	# def create(self,vals):
	# 	_logger.critical('create self = {}'.format(self))
	# 	_logger.critical('create vals = {}'.format(vals))
	# 	res = super(construction_change_order_extend,self).create(vals)
	# 	_logger.critical('create res = {}'.format(res))
	# 	if res:
	# 		budget_obj = self.env['so_vo.budget_change'].create({
	# 				'contract_id':res.analytic_account_id.id,
	# 				'name':res.name,
	# 				'types':res.so_reference.id,
	# 				'reqstr_id':res.user_id.id,
	# 				'apprvr_id':res.approve_by.id,
	# 				'date_apprv':res.approve_date,
	# 				'old_amount':res.original_contract_amount,
	# 				'new_amount':res.total_contract_amount_all_change
	# 			})
	# 	return res
	# @api.multi
	# def write(self,vals):
	# 	_logger.critical('write self = {}'.format(self))
	# 	_logger.critical('write vals = {}'.format(vals))
	# 	res = super(construction_change_order_extend,self).write(vals)
	# 	_logger.critical('write res = {}'.format(res))
	# 	if vals.get('original_contract_amount'):
	# 		budget_obj = self.env['so_vo.budget_change'].create({
	# 				'contract_id':vals.get('analytic_account_id',self.analytic_account_id).id,
	# 				'name':vals.get('name',self.name),
	# 				'types':vals.get('so_reference',self.so_reference).id,
	# 				'reqstr_id':vals.get('user_id',self.user_id).id,
	# 				'apprvr_id':vals.get('approve_by',self.approve_by).id,
	# 				'date_apprv':vals.get('approve_date',self.approve_date),
	# 				'old_amount':vals.get('original_contract_amount',self.original_contract_amount),
	# 				'new_amount':vals.get('total_contract_amount_all_change',self.total_contract_amount_all_change)
	# 			})
	# 	return res

class contract_account_analytic_account(models.Model):
	_inherit = 'account.analytic.account'

	variation_table = fields.One2many('construction.change.order', 'analytic_account_id', 'Variation Order', copy=True)
	# variation_table = fields.One2many('sale.order', 'project_id', 'Variation Order', copy=True)
	budget_change_hist = fields.One2many('so_vo.budget_change', 'contract_id', 'Budget Change History', copy=True)


class so_vo_variation_order(models.Model):
	_name = 'so_vo.budget_change'

	contract_id = fields.Many2one('account.analytic.account', string="Contract ID")
	name = fields.Char('Budget Change Name')
	types = fields.Char('Budget Change Type')
	reqstr_id = fields.Many2one('res.users', string="Requester")
	apprvr_id = fields.Many2one('res.users', string="Approver")
	date_apprv = fields.Date('Date Approved')
	old_amount = fields.Float('Old Planned Amount')
	new_amount = fields.Float('New Planned Amount')

	# @api.depends('construction_contracting_change_order.name','construction_contracting_change_order.so_reference','construction_contracting_change_order.user_id',
	# 	'construction_contracting_change_order.approve_by','construction_contracting_change_order.approve_date','construction_contracting_change_order.original_contract_amount',
	# 	'construction_contracting_change_order.total_contract_amount_all_change','construction_contracting_change_order.analytic_account_id')
	# 'construction_contracting_change_order.id',
	#alt way

	# didnt work out
	# @api.one
	# @api.depends('construction_contracting_change_order.total_contract_amount_all_change')
	# def _changed_planned_amount(self):
	# 	_logger.warning('_changed_planned_amount START')
	# 	_logger.warning(self)
	# 	_logger.warning(construction_contracting_change_order.id)
	# 	_logger.warning(construction_contracting_change_order.total_contract_amount_all_change)
		
	# 	construction_obj = self.env['construction_contracting_change_order'].browse(construction_contracting_change_order.id)
	# 	_logger.warning('construction_obj w=w {}'%(construction_obj))
	# 	account_obj = self.env['account.analytic.account'].browse(construction_obj.analytic_account_id)
	# 	_logger.warning('account_obj w=w {}'%(account_obj))
	# 	if account_obj:
	# 		self_obj = self.create({
	# 				'contract_id':account_obj.id,
	# 				'name':construction_obj.name,
	# 				'types':construction_obj.so_reference,
	# 				'reqstr_id':construction_obj.user_id,
	# 				'apprvr_id':construction_obj.approve_by,
	# 				'date_apprv':construction_obj.approve_date,
	# 				'old_amount':construction_obj.original_contract_amount,
	# 				'new_amount':construction_obj.total_contract_amount_all_change
	# 			})
	# 	_logger.warning('_changed_planned_amount END')

